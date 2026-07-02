import logging
import os

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
)

logger = logging.getLogger(__name__)


class VectorService:

    COLLECTION_NAME = "shl_assessments"

    def __init__(self):
        self.client = QdrantClient(
            url=os.getenv("QDRANT_URL"),
            api_key=os.getenv("QDRANT_API_KEY"),
        )

    def create_collection(self):
        collections = self.client.get_collections().collections
        names = [c.name for c in collections]

        if self.COLLECTION_NAME not in names:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=768,
                    distance=Distance.COSINE,
                ),
            )
            logger.info("Collection '%s' created.", self.COLLECTION_NAME)
        else:
            logger.info("Collection '%s' already exists.", self.COLLECTION_NAME)

    def upload_points(self, points: list[PointStruct]):
        self.client.upsert(
            collection_name=self.COLLECTION_NAME,
            points=points,
        )

    def search(self, vector, limit=5):
        return self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=vector,
            limit=limit,
        )