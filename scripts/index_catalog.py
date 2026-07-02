"""
Re-index all assessments into Qdrant using Gemini gemini-embedding-001 (768 dims).

Run this script once after deploying or whenever the catalog changes:
    python -m scripts.index_catalog

Rate limit: free tier allows 100 requests/min, so this script batches with
a 65-second pause between batches to stay under the limit.
"""

import json
import time

from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.services.embedding_service import EmbeddingService
from app.services.vector_service import VectorService

COLLECTION_NAME = VectorService.COLLECTION_NAME
BATCH_SIZE = 90  # stay safely under 100 req/min
BATCH_PAUSE = 65  # seconds to wait between batches

embedding_service = EmbeddingService()
vector_service = VectorService()

# Drop and recreate the collection so the vector size is always correct
collections = vector_service.client.get_collections().collections
existing = [c.name for c in collections]

if COLLECTION_NAME in existing:
    vector_service.client.delete_collection(COLLECTION_NAME)
    print(f"Deleted existing collection '{COLLECTION_NAME}'.")

vector_service.client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=768,
        distance=Distance.COSINE,
    ),
)
print(f"Created collection '{COLLECTION_NAME}' with 768-dim vectors.\n")

with open("app/data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

points = []
total = len(catalog)

for i, assessment in enumerate(catalog):
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

    print(f"  [{i + 1}/{total}] Embedded: {assessment.get('name')}", flush=True)

    # Upload in batches and pause to respect rate limits
    if len(points) == BATCH_SIZE:
        vector_service.upload_points(points)
        print(f"\nUploaded batch of {BATCH_SIZE}. Pausing {BATCH_PAUSE}s for rate limit...\n", flush=True)
        points = []
        time.sleep(BATCH_PAUSE)

# Upload any remaining points
if points:
    vector_service.upload_points(points)
    print(f"\nUploaded final batch of {len(points)}.", flush=True)

print(f"\nDone. Indexed {total} assessments into Qdrant.")
