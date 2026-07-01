from app.services.search_service import SearchService

service = SearchService()

results = service.search("reasoning")

for assessment in results:
    print(assessment.name)
