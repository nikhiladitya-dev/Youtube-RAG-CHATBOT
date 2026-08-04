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

        self.transcript_service = TranscriptService()
        self.document_processor = DocumentProcessor()
        self.embedding_service = EmbeddingService()
        self.vectorstore_service = VectorStoreService(self.embedding_service)

        self.retrieval_service = RetrievalService(self.vectorstore_service)
        self.llm_service = LLMService()
        self.history_service = HistoryService()
        self.question_rewriter = QuestionRewriter(self.llm_service)

        self.rag_chain = RAGChain(
            retrieval_service=self.retrieval_service,
            llm_service=self.llm_service,)

        self.chat_service = ChatService(
            rag_chain=self.rag_chain,
            history_service=self.history_service,
            question_rewriter=self.question_rewriter,)

container = ServiceContainer()