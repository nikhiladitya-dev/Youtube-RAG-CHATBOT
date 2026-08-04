from langchain_huggingface import HuggingFaceEmbeddings
from app.core.config import settings
from app.core.logger import logger

class EmbeddingService:

    def __init__(self):
        logger.info("Loading embedding model...")
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={
                "device": "cpu"
            },
            encode_kwargs={
                "normalize_embeddings": True
            }
        )
        logger.info("Embedding model loaded successfully.")

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents.
        """

        logger.info(
            f"Generating embeddings for {len(texts)} documents..."
        )

        embeddings = self.embedding_model.embed_documents(
            texts
        )

        logger.info("Document embeddings generated successfully.")

        return embeddings

    def embed_query(
        self,
        query: str,
    ) -> list[float]:
        """
        Generate an embedding for a user query.
        """

        logger.info("Generating query embedding...")

        embedding = self.embedding_model.embed_query(
            query
        )

        logger.info("Query embedding generated successfully.")

        return embedding

    def get_embedding_model(
        self,
    ) -> HuggingFaceEmbeddings:
        """
        Return the configured embedding model.
        """

        return self.embedding_model
