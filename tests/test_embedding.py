from app.services.embedding_service import EmbeddingService

service = EmbeddingService()

vector = service.embed("Python developer with SQL knowledge")

print(type(vector))
print(len(vector))
print(vector[:5])