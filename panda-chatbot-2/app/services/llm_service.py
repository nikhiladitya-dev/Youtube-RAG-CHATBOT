from langchain_huggingface import (
    HuggingFaceEndpoint,
    ChatHuggingFace,
)
from app.core.config import settings
from app.core.logger import logger

class LLMService:

    def __init__(self):
        logger.info("Loading LLM...")
        endpoint = HuggingFaceEndpoint(
            repo_id=settings.LLM_MODEL,
            huggingfacehub_api_token=settings.HF_TOKEN,
            temperature=settings.LLM_TEMPERATURE,
            max_new_tokens=settings.LLM_MAX_NEW_TOKENS,
        )

        self.llm = ChatHuggingFace(
            llm=endpoint
        )
        logger.info("LLM loaded successfully.")

    def invoke(
        self,
        prompt: str,
    ) -> str:
        #  Invoke the LLM with a prompt.

        logger.info("Invoking LLM...")
        response = self.llm.invoke(prompt)

        return response.content

    def get_llm(
        self,
    ) -> ChatHuggingFace:
        # Return the configured LLM.

        return self.llm

    