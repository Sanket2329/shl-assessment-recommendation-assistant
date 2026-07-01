from app.services.catalog_service import CatalogService


class SearchService:
    def __init__(self):
        self.catalog = CatalogService().get_all()

    def search(self, query: str):
        query = query.lower()

        results = []

        for assessment in self.catalog:
            searchable_text = " ".join([
                assessment.name,
                assessment.description,
                assessment.category,
                assessment.test_type,
                " ".join(assessment.skills)
            ]).lower()

            if query in searchable_text:
                results.append(assessment)

        return results