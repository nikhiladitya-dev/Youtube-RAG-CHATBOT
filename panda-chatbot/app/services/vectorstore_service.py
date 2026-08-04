from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.core.config import settings
from app.core.logger import logger
from app.services.embedding_service import EmbeddingService

class VectorStoreService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
#   Initialize the persistent Chroma vector store.

        logger.info("Initializing Chroma vector store...")
        self.embedding_service = embedding_service
        self.vector_store = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embedding_service.get_embedding_model(),
            persist_directory=settings.CHROMA_DB_PATH,
        )
        logger.info("Chroma vector store initialized successfully.")

    def add_documents(
        self,
        documents: list[Document],
    ) -> None:
        """
        Add documents to the vector database.
        """

        logger.info(
            f"Adding {len(documents)} documents to ChromaDB..."
        )

        self.vector_store.add_documents(documents)

        logger.info("Documents indexed successfully.")

    def similarity_search(
        self,
        query: str,
        k: int = 4,
    ) -> list[Document]:
        # Perform similarity search.

        logger.info(f"Searching top {k} similar documents...")

        documents = self.vector_store.similarity_search(
            query=query,
            k=k,
        )

        logger.info(f"Retrieved {len(documents)} documents.")
        return documents

    def mmr_search(
        self,
        query: str,
        video_id: str,
        k: int = 4,
        fetch_k: int = 20,
        
    ) -> list[Document]:
        # Perform Max Marginal Relevance search.
        logger.info( f"Performing MMR search (k={k}, fetch_k={fetch_k})...")

        documents = self.vector_store.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
            filter = {"video_id":video_id,},
        )
        logger.info(f"Retrieved {len(documents)} documents.")
        return documents
    
    def delete_collection(
        self,
    ) -> None:
        
        # Delete the Chroma collection.

        logger.warning("Deleting Chroma collection...")
        self.vector_store.delete_collection()
        logger.info("Collection deleted successfully.")

    def get_collection_count(
        self,
    ) -> int:
        
        # Return the number of indexed documents.

        return self.vector_store._collection.count()   

    def get_vector_store(
        self,
    ) -> Chroma:
        # Return the Chroma vector store.
        return self.vector_store 

    def is_video_indexed(
        self,
        video_id: str,
    ) -> bool:
        
        # Check whether a video's chunks are already indexed.

        results = self.vector_store.get(
            where={
                "video_id": video_id,
            }
        )
        return len(results["ids"]) > 0
    
    