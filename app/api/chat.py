import json

from fastapi import APIRouter

from app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Recommendation,
)
from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.vector_service import VectorService

router = APIRouter()


def get_match_score(score: float, name: str) -> str:
    name = name.lower()

    if "live coding" in name:
        return "High"

    if "framework" in name:
        return "High"

    if score >= 0.45:
        return "High"
    elif score >= 0.35:
        return "Medium"

    return "Low"


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    print("Chat request received", flush=True)

    embedding_service = EmbeddingService()
    vector_service = VectorService()
    llm_service = LLMService()

    conversation_context = "\n".join(
        f"{message.role}: {message.content}"
        for message in request.messages
    )

    latest_message = request.messages[-1].content
    query = latest_message.lower()

    shl_keywords = [
        "assessment",
        "test",
        "candidate",
        "hiring",
        "recruit",
        "developer",
        "engineer",
        "manager",
        "sales",
        "java",
        "python",
        "sql",
        "leadership",
        "personality",
        "behavior",
        "cognitive",
        "compare",
        "difference",
        "skills",
        "role",
        "job",
    ]

    is_shl_query = any(keyword in query for keyword in shl_keywords)

    comparison_keywords = ["compare", "difference", "vs", "versus"]
    is_comparison = any(keyword in query for keyword in comparison_keywords)

    vague_queries = [
        "assessment",
        "test",
        "recommend assessment",
        "recommend test",
        "i need an assessment",
        "i need a test",
    ]

    if any(q == query.strip() for q in vague_queries):
        return ChatResponse(
            reply=(
                "I'd be happy to help. Could you tell me:\n\n"
                "• What role are you hiring for?\n"
                "• Which skills would you like to assess?\n"
                "• What seniority level is the role?"
            ),
            recommendations=[],
        )

    # Comparison detection
    if is_comparison:
        with open("app/data/catalog.json", "r") as f:
            catalog = json.load(f)

        matched = [
            assessment
            for assessment in catalog
            if assessment["name"].lower() in query
        ]

        if len(matched) >= 2:
            comparison = llm_service.compare(matched[0], matched[1])
            return ChatResponse(reply=comparison, recommendations=[])

    # Reject non-SHL queries
    if not is_shl_query:
        return ChatResponse(
            reply=(
                "I'm designed to help recommend and compare SHL assessments. "
                "Please provide a hiring requirement, job description, "
                "or ask about SHL assessments."
            ),
            recommendations=[],
        )

    # Generate embedding and search
    print("Generating embedding...", flush=True)
    query_vector = embedding_service.embed(conversation_context)

    print("Searching Qdrant...", flush=True)
    results = vector_service.search(query_vector, limit=10)

    assessments = []
    for point in results.points:
        payload = point.payload.copy()
        payload["retrieval_score"] = round(point.score, 3)
        assessments.append(payload)

    # Gemini recommendations
    print("Calling Gemini...", flush=True)
    result = llm_service.recommend(
        conversation_context,
        latest_message,
        assessments,
    )
    print("Gemini complete", flush=True)

    payload_lookup = {item["name"]: item for item in assessments}

    recommendations = []
    for item in result["recommendations"][:5]:
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

    return ChatResponse(
        reply=result["summary"],
        recommendations=recommendations,
    )
