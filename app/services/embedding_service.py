class EmbeddingService:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            print("STEP 1", flush=True)

            from sentence_transformers import SentenceTransformer

            print("STEP 2", flush=True)

            cls._model = SentenceTransformer("models/all-MiniLM-L6-v2")

            print("STEP 3", flush=True)

        return cls._model

    def embed(self, text):
        return self.get_model().encode(text).tolist()