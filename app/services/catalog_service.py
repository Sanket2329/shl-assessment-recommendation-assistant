import json
from pathlib import Path

from app.models import Assessment


class CatalogService:

    def __init__(self):
        self.catalog_path = Path("app/data/catalog.json")

    def get_all(self):

        with open(self.catalog_path, "r") as file:
            data = json.load(file)

        return [Assessment(**item) for item in data]