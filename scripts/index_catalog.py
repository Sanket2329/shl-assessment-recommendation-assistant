import json

from qdrant_client.models import PointStruct

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService


embedding_service = EmbeddingService()
vector_service = VectorService()

vector_service.create_collection()

with open("app/data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

points = []

for assessment in catalog:

    searchable_text = " ".join(
        [
            assessment.get("name", ""),
            assessment.get("description", ""),
            " ".join(assessment.get("keys", [])),
            " ".join(assessment.get("job_levels", [])),
            " ".join(assessment.get("languages", [])),
        ]
    )

    vector = embedding_service.embed(searchable_text)

    payload = {
        "entity_id": assessment.get("entity_id"),
        "name": assessment.get("name"),
        "description": assessment.get("description"),
        "url": assessment.get("link"),
        "duration": assessment.get("duration"),
        "remote": assessment.get("remote"),
        "adaptive": assessment.get("adaptive"),
        "job_levels": assessment.get("job_levels"),
        "languages": assessment.get("languages"),
        "keys": assessment.get("keys"),
    }

    points.append(
        PointStruct(
            id=int(assessment["entity_id"]),
            vector=vector,
            payload=payload,
        )
    )

vector_service.upload_points(points)

print(f"Indexed {len(points)} assessments.")