from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService
from app.services.llm_service import LLMService

query = "Looking for a Java backend developer with strong problem solving skills"

embedding_service = EmbeddingService()
vector_service = VectorService()
llm_service = LLMService()

query_vector = embedding_service.embed(query)

results = vector_service.search(query_vector, limit=5)

assessments = []

for point in results.points:
    assessments.append(point.payload)

response = llm_service.recommend(query, assessments)

print(response)