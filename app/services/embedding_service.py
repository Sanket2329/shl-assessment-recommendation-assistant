class EmbeddingService:
    def __init__(self):
        self.model = None

    def embed(self, text: str):
        if self.model is None:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer("all-MiniLM-L6-v2")

        return self.model.encode(text).tolist()