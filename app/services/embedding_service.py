class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print("Importing SentenceTransformer...", flush=True)

            from sentence_transformers import SentenceTransformer

            print("Loading model...", flush=True)

            cls._model = SentenceTransformer("models/all-MiniLM-L6-v2")

            print("Model loaded.", flush=True)

        return cls._model

    def embed(self, text: str):
        return self.get_model().encode(text).tolist()