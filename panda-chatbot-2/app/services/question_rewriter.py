from app.core.logger import logger
from app.prompts.history_prompt import HISTORY_PROMPT
from app.services.llm_service import LLMService
from app.models.conversation_models import Conversation


class QuestionRewriter:

    def __init__(
        self,
        llm_service: LLMService,
    ):

        self.llm_service = llm_service

    def rewrite(
        self,
        history: Conversation,
        question: str,
    ) -> str:
        
        # Rewrite a follow-up question into a standalone question.

        logger.info("Rewriting question...")

        history_text = self._format_history(history)

        prompt = HISTORY_PROMPT.invoke(
            {
                "history": history_text,
                "question": question,
            }
        )

        rewritten_question = self.llm_service.invoke(prompt)

        logger.info(f"Rewritten Question: {rewritten_question}")
        return rewritten_question.strip()

    def _format_history(
        self,
        history: Conversation,
    ) -> str:
        # Convert conversation history into text.
        if not history.messages:
            return "No previous conversation."

        lines = []

        for message in history.messages:
            lines.append(f"{message.role.title()}: {message.content}")

        return "\n".join(lines)