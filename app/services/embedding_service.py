class EmbeddingService:
    def __init__(self):
        self.model = None

    def embed(self, text: str):
        print("Embedding: before importing SentenceTransformer", flush=True)

        from sentence_transformers import SentenceTransformer

        print("Embedding: SentenceTransformer imported", flush=True)

        if self.model is None:
            print("Embedding: before model load", flush=True)
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
            print("Embedding: model loaded", flush=True)

        print("Embedding: before encode", flush=True)

        vector = self.model.encode(text)

        print("Embedding: encode complete", flush=True)

        return vector.tolist()