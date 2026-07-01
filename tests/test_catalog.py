from app.services.catalog_service import CatalogService

service = CatalogService()

catalog = service.get_all()

for assessment in catalog:
    print(assessment.name)