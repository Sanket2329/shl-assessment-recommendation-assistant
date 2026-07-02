from sentence_transformers import SentenceTransformer


class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer("models/all-MiniLM-L6-v2")
        return cls._model

    def embed(self, text: str):
        return self.get_model().encode(text).tolist()