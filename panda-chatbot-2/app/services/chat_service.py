from app.chains.rag_chain import RAGChain
from app.core.logger import logger
from app.services.history_service import HistoryService
from app.services.question_rewriter import QuestionRewriter

class ChatService:

    def __init__(
        self,
        rag_chain: RAGChain,
        history_service: HistoryService,
        question_rewriter: QuestionRewriter,
    ):

        self.rag_chain = rag_chain
        self.history_service = history_service
        self.question_rewriter = question_rewriter

    def ask(
        self,
        question: str,
        video_id: str,
    ):

        history = self.history_service.get_history()
        standalone_question = self.question_rewriter.rewrite(
            history,
            question,
        )
        response = self.rag_chain.invoke(
            question= standalone_question,
            video_id= video_id,
        )
        self.history_service.add_user_message(question)
        self.history_service.add_assistant_message(
            response["answer"]
        )
        return response