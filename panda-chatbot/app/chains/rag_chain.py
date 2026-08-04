from langchain_core.documents import Document
from app.core.logger import logger
from app.prompts.rag_prompt import RAG_PROMPT
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.utils.timestamp_utils import (format_timestamp_range, )

class RAGChain:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
    ):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def invoke(
        self,
        question: str,
        video_id: str
    ) -> dict:
        # Execute the complete RAG pipeline.
        if not question.strip():
            raise ValueError("Question cannot be empty.")
        
        logger.info("Running RAG chain...")
        documents = self.retrieval_service.retrieve(query=question, video_id= video_id)

        context = self._format_context(documents)

        prompt = RAG_PROMPT.invoke(
            {
                "context": context,
                "question": question,
            }
        )

        answer = self.llm_service.invoke(prompt)

        logger.info("RAG response generated successfully.")

        return {
            "answer": answer,
            "sources": [
                {
                    "start_time": document.metadata["start_time"],
                    "end_time": document.metadata["end_time"],
                    "timestamp": format_timestamp_range(
                        document.metadata["start_time"],
                        document.metadata["end_time"],
                    ),
                    "content": document.page_content,
                }
                for document in documents
            ],
        }

    def _format_context(
        self,
        documents: list[Document],
    ) -> str:
        # Convert retrieved documents into a prompt-friendly context string.

        logger.info("Formatting retrieved context...")
        sections = []
        for document in documents:

            start = document.metadata["start_time"]
            end = document.metadata["end_time"]
            section = (
                f"[Timestamp: "
                f"{format_timestamp_range(start, end)}]\n\n"
                f"{document.page_content}"
            )
            sections.append(section)
        return "\n\n" + ("-" * 60) + "\n\n".join(sections)

    