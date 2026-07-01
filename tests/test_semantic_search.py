from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

embedding_service = EmbeddingService()
vector_service = VectorService()

query = "Looking for a Java backend developer with strong problem solving skills"

query_vector = embedding_service.embed(query)

results = vector_service.search(query_vector, limit=5)

for point in results.points:
    print("=" * 60)
    print("Score:", round(point.score, 3))
    print("Name:", point.payload["name"])
    print("Duration:", point.payload["duration"] or "Not specified")
    print("Remote:", point.payload["remote"])
    print("Adaptive:", point.payload["adaptive"])
    print("Keys:", point.payload["keys"])