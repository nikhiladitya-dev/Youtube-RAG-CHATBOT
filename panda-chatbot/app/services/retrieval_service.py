from langchain_core.documents import Document
from app.core.logger import logger
from app.services.vectorstore_service import (VectorStoreService,)

class RetrievalService:
    def __init__(
        self,
        vector_store_service: VectorStoreService,
    ):

        self.vector_store_service = vector_store_service
    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:
        # Retrieve documents using similarity search.
        logger.info("Performing similarity retrieval...")
        return self.vector_store_service.similarity_search(
            query=query, k=k,)

    def retrieve(
        self,
        query: str,
        video_id: str,
        k: int = 4,
    ) -> list[Document]:
        #  Retrieve the most relevant documents.
        return self.mmr_search(
            query=query,video_id=video_id, k=k)

    def mmr_search(
        self,
        query: str,
        video_id: str,
        k: int = 4,
        fetch_k: int = 20,
    ) -> list[Document]:
        #  Retrieve documents using Max Marginal Relevance.

        logger.info( "Performing MMR retrieval...")
        return self.vector_store_service.mmr_search(
            query=query,video_id=video_id , k=k, fetch_k=fetch_k,
        )


    