from sentence_transformers import SentenceTransformer


class EmbeddingService:
    def __init__(self):
        self.model = None

    def embed(self, text: str):
        if self.model is None:
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

        return self.model.encode(text).tolist()