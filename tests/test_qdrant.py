from app.services.vector_service import VectorService

service = VectorService()

service.create_collection()

print(service.client.get_collections())