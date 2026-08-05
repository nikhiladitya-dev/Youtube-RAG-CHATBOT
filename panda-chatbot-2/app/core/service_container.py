from app.core.logger import logger

from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.services.history_service import HistoryService
from app.services.question_rewriter import QuestionRewriter
from app.chains.rag_chain import RAGChain
from app.services.chat_service import ChatService
from app.services.transcript_service import TranscriptService
from app.services.document_processor import DocumentProcessor


class ServiceContainer:

    def __init__(self):

        self.embedding_service = None
        self.vectorstore_service = None
        self.retrieval_service = None
        self.llm_service = None
        self.history_service = None
        self.question_rewriter = None
        self.rag_chain = None
        self.chat_service = None

        self.transcript_service = None
        self.document_processor = None

        self.current_video_id = None

    def initialize(self):

        logger.info("Initializing core services...")

        self.transcript_service = TranscriptService()

        self.document_processor = DocumentProcessor()

        self.history_service = HistoryService()

        logger.info("Core services initialized successfully.")


    def get_embedding_service(self):

        if self.embedding_service is None:

            logger.info("Creating EmbeddingService...")

            self.embedding_service = EmbeddingService()

        return self.embedding_service

    def get_vectorstore_service(self):

        if self.vectorstore_service is None:

            logger.info("Creating VectorStoreService...")

            self.vectorstore_service = VectorStoreService(
                self.get_embedding_service()
            )

        return self.vectorstore_service

    def get_retrieval_service(self):

        if self.retrieval_service is None:

            logger.info("Creating RetrievalService...")

            self.retrieval_service = RetrievalService(
                self.get_vectorstore_service()
            )

        return self.retrieval_service

    def get_llm_service(self):

        if self.llm_service is None:

            logger.info("Creating LLMService...")

            self.llm_service = LLMService()

        return self.llm_service

    def get_question_rewriter(self):

        if self.question_rewriter is None:

            logger.info("Creating QuestionRewriter...")

            self.question_rewriter = QuestionRewriter(
                self.get_llm_service()
            )

        return self.question_rewriter

    def get_rag_chain(self):

        if self.rag_chain is None:

            logger.info("Creating RAGChain...")

            self.rag_chain = RAGChain(
                retrieval_service=self.get_retrieval_service(),
                llm_service=self.get_llm_service(),
            )

        return self.rag_chain

    def get_chat_service(self):

        if self.chat_service is None:

            logger.info("Creating ChatService...")

            self.chat_service = ChatService(
                rag_chain=self.get_rag_chain(),
                history_service=self.history_service,
                question_rewriter=self.get_question_rewriter(),
            )

        return self.chat_service


container = ServiceContainer()