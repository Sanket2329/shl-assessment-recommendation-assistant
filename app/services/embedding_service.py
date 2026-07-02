import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

EMBEDDING_MODEL = "models/gemini-embedding-001"
EMBEDDING_DIMENSIONS = 768


class EmbeddingService:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            api_key = os.getenv("GEMINI_API_KEY")

            if not api_key:
                raise ValueError("GEMINI_API_KEY not found")

            cls._client = genai.Client(api_key=api_key)

        return cls._client

    def embed(self, text: str) -> list[float]:
        client = self.get_client()

        response = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=text,
            config=types.EmbedContentConfig(
                output_dimensionality=EMBEDDING_DIMENSIONS,
            ),
        )

        return response.embeddings[0].values
