import json
import logging

from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Recommendation,
)
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService

logger = logging.getLogger(__name__)

router = APIRouter()

# ---------------------------------------------------------------------------
# Keyword sets
# ---------------------------------------------------------------------------

SHL_KEYWORDS = {
    "assessment", "test", "candidate", "hiring", "recruit",
    "developer", "engineer", "manager", "sales", "java", "python",
    "sql", "leadership", "personality", "behavior", "cognitive",
    "compare", "difference", "skills", "role", "job", "description",
    "jd", "experience", "senior", "junior", "mid", "graduate",
    "intern", "analyst", "architect", "devops", "data", "science",
    "ml", "ai", "frontend", "backend", "fullstack", "testing", "qa",
}

COMPARISON_KEYWORDS = {"compare", "difference", "vs", "versus"}

# Queries that are so vague we must ask for more detail before searching
VAGUE_QUERIES = {
    "assessment",
    "test",
    "recommend assessment",
    "recommend test",
    "i need an assessment",
    "i need a test",
    "suggest assessment",
    "suggest test",
}

# Prompt-injection patterns — phrases that try to redirect the assistant
INJECTION_PATTERNS = [
    "ignore previous",
    "ignore all previous",
    "disregard previous",
    "forget previous",
    "forget your instructions",
    "you are now",
    "act as",
    "pretend you are",
    "new instructions",
    "system prompt",
    "jailbreak",
    "override",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_match_score(score: float, name: str) -> str:
    name_lower = name.lower()

    if "live coding" in name_lower:
        return "High"
    if "framework" in name_lower:
        return "High"
    if score >= 0.45:
        return "High"
    if score >= 0.35:
        return "Medium"
    return "Low"


def is_prompt_injection(text: str) -> bool:
    lower = text.lower()
    return any(pattern in lower for pattern in INJECTION_PATTERNS)


def is_shl_related(text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in SHL_KEYWORDS)


def is_comparison_request(text: str) -> bool:
    lower = text.lower()
    return any(keyword in lower for keyword in COMPARISON_KEYWORDS)


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info("Chat request received — %d message(s)", len(request.messages))

    embedding_service = EmbeddingService()
    vector_service = VectorService()
    llm_service = LLMService()

    latest_message = request.messages[-1].content
    query = latest_message.strip()
    query_lower = query.lower()

    # Build full conversation context for embedding + LLM
    conversation_context = "\n".join(
        f"{msg.role}: {msg.content}"
        for msg in request.messages
    )

    # ------------------------------------------------------------------
    # Guard: prompt injection
    # ------------------------------------------------------------------
    if is_prompt_injection(query):
        logger.warning("Prompt injection attempt detected")
        return ChatResponse(
            reply=(
                "I'm only able to help with SHL assessment recommendations. "
                "I can't follow instructions that ask me to change my behavior "
                "or recommend products outside the SHL catalog."
            ),
            recommendations=[],
            end_of_conversation=False,
        )

    # ------------------------------------------------------------------
    # Guard: off-topic query
    # ------------------------------------------------------------------
    if not is_shl_related(query):
        logger.info("Off-topic query rejected")
        return ChatResponse(
            reply=(
                "That question is outside my scope. I'm here to help you find "
                "the right SHL assessments for your hiring needs. Try asking "
                "something like: \"Recommend assessments for a Python developer\" "
                "or \"What should I use for a senior sales role?\""
            ),
            recommendations=[],
            end_of_conversation=False,
        )

    # ------------------------------------------------------------------
    # Guard: vague query — ask for clarification
    # ------------------------------------------------------------------
    if query_lower in VAGUE_QUERIES:
        logger.info("Vague query — requesting clarification")
        return ChatResponse(
            reply=(
                "I'd be happy to help. Could you share a bit more detail?\n\n"
                "• What role are you hiring for?\n"
                "• Which skills or competencies matter most?\n"
                "• What seniority level is the position?\n"
                "• Are you looking for technical, behavioral, or both types of assessments?"
            ),
            recommendations=[],
            end_of_conversation=False,
        )

    # ------------------------------------------------------------------
    # Comparison flow
    # ------------------------------------------------------------------
    if is_comparison_request(query):
        logger.info("Comparison request detected")

        with open("app/data/catalog.json", "r") as f:
            catalog = json.load(f)

        matched = [
            a for a in catalog
            if a["name"].lower() in query_lower
        ]

        if len(matched) >= 2:
            comparison = llm_service.compare(matched[0], matched[1])
            return ChatResponse(
                reply=comparison,
                recommendations=[],
                end_of_conversation=False,
            )

        # Could not match two assessments by name — fall through to
        # semantic search so we can still return something useful

    # ------------------------------------------------------------------
    # Main flow: semantic search + LLM recommendation
    # ------------------------------------------------------------------
    logger.info("Generating query embedding")
    query_vector = embedding_service.embed(conversation_context)

    logger.info("Querying Qdrant vector store")
    results = vector_service.search(query_vector, limit=10)

    assessments = []
    for point in results.points:
        payload = point.payload.copy()
        payload["retrieval_score"] = round(point.score, 3)
        assessments.append(payload)

    logger.info("Calling Gemini for recommendations")
    result = llm_service.recommend(
        conversation_context,
        latest_message,
        assessments,
    )
    logger.info("Gemini recommendation complete")

    payload_lookup = {item["name"]: item for item in assessments}

    recommendations = []
    for item in result["recommendations"][:10]:
        payload = payload_lookup.get(item["assessment_name"])

        if not payload:
            continue

        recommendations.append(
            Recommendation(
                name=payload["name"],
                url=payload["url"],
                duration=payload["duration"],
                remote=payload["remote"],
                adaptive=payload["adaptive"],
                retrieval_score=payload["retrieval_score"],
                match_score=get_match_score(
                    payload["retrieval_score"],
                    payload["name"],
                ),
                reason=item["reason"],
            )
        )

    # Sort by retrieval_score descending (Option B) so the order always
    # reflects semantic relevance, regardless of LLM re-ranking
    recommendations.sort(
        key=lambda r: r.retrieval_score or 0.0,
        reverse=True,
    )

    # Cap at 10 as per evaluation criteria
    recommendations = recommendations[:10]

    return ChatResponse(
        reply=result["summary"],
        recommendations=recommendations,
        end_of_conversation=False,
    )
