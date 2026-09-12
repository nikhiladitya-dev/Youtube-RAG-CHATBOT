import json
import logging
from pathlib import Path

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
)
from deepeval.test_case import LLMTestCase

from app.services.embedding_service import EmbeddingService
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.vectorstore_service import VectorStoreService

from evals.component.ollama_judge import OllamaJudge


# =============================================================================
# Configuration
# =============================================================================

BASE_DIR = Path(__file__).resolve().parents[2]

GOLDEN_DATASET_PATH = (
    BASE_DIR / "evals" / "datasets" / "golden_dataset.json"
)

VIDEO_ID = "8hly31xKli0"

# None = evaluate the complete golden dataset
NUM_TEST_CASES = None

THRESHOLD = 0.70

JUDGE_MODEL = "qwen3:4b"


# =============================================================================
# Logging
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# =============================================================================
# Load Golden Dataset
# =============================================================================

def load_golden_dataset() -> list[dict]:

    logger.info(
        f"Loading golden dataset from: {GOLDEN_DATASET_PATH}"
    )

    with open(
        GOLDEN_DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:

        dataset = json.load(file)

    if not dataset:
        raise ValueError("Golden dataset is empty.")

    logger.info(
        f"Loaded {len(dataset)} golden test cases."
    )

    return dataset


# =============================================================================
# Initialize Production RAG Components
# =============================================================================

def initialize_rag_chain():

    logger.info("Initializing production RAG components...")

    embedding_service = EmbeddingService()

    vector_store_service = VectorStoreService(
        embedding_service=embedding_service
    )

    retrieval_service = RetrievalService(
        vector_store_service=vector_store_service
    )

    llm_service = LLMService()

    from app.chains.rag_chain import RAGChain

    rag_chain = RAGChain(
        retrieval_service=retrieval_service,
        llm_service=llm_service,
    )

    logger.info("Production RAG chain initialized.")

    return rag_chain


# =============================================================================
# Build Generator Test Cases
# =============================================================================

def build_test_cases(
    dataset: list[dict],
    rag_chain,
) -> list[LLMTestCase]:

    test_cases = []

    # Evaluate the complete golden dataset
    if NUM_TEST_CASES is None:
        selected_dataset = dataset
        evaluation_mode = "FULL GOLDEN DATASET"
    else:
        selected_dataset = dataset[:NUM_TEST_CASES]
        evaluation_mode = f"LIMITED ({NUM_TEST_CASES} CASES)"

    logger.info(
        f"Generator evaluation mode: {evaluation_mode}"
    )

    logger.info(
        f"Preparing {len(selected_dataset)} generator test cases."
    )

    for index, item in enumerate(selected_dataset):

        question = item["question"]
        ideal_answer = item["ideal_answer"]

        logger.info(
            f"Generating answer for test case "
            f"{index + 1}/{len(selected_dataset)}: "
            f"{question}"
        )

        try:

            response = rag_chain.invoke(
                question=question,
                video_id=VIDEO_ID,
            )

        except Exception:

            logger.exception(
                f"RAG generation failed for test case {index}."
            )

            raise

        actual_answer = response.get("answer")

        sources = response.get("sources", [])

        retrieval_context = [
            source["content"]
            for source in sources
        ]

        if not actual_answer:
            raise ValueError(
                f"Empty generated answer for test case {index}."
            )

        if not retrieval_context:
            raise ValueError(
                f"No retrieval context returned for "
                f"test case {index}."
            )

        logger.info(
            f"Generated answer successfully for "
            f"test case {index + 1}."
        )

        logger.info(
            f"Retrieved {len(retrieval_context)} "
            f"context chunks."
        )

        test_case = LLMTestCase(
            input=question,
            expected_output=ideal_answer,
            actual_output=actual_answer,
            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

    logger.info(
        f"Successfully prepared "
        f"{len(test_cases)} DeepEval test cases."
    )

    return test_cases


# =============================================================================
# Main Evaluation
# =============================================================================

def main():

    logger.info("=" * 80)
    logger.info("GENERATOR EVALUATION - FULL GOLDEN DATASET")
    logger.info("=" * 80)

    logger.info(
        f"Evaluation judge: Ollama/{JUDGE_MODEL}"
    )

    logger.info(
        f"Faithfulness threshold: {THRESHOLD}"
    )

    logger.info(
        f"Answer Relevance threshold: {THRESHOLD}"
    )

    # -------------------------------------------------------------------------
    # Load dataset
    # -------------------------------------------------------------------------

    dataset = load_golden_dataset()

    # -------------------------------------------------------------------------
    # Initialize production RAG chain
    # -------------------------------------------------------------------------

    rag_chain = initialize_rag_chain()

    # -------------------------------------------------------------------------
    # Generate answers and construct DeepEval test cases
    # -------------------------------------------------------------------------

    test_cases = build_test_cases(
        dataset=dataset,
        rag_chain=rag_chain,
    )

    # -------------------------------------------------------------------------
    # Initialize local evaluation judge
    # -------------------------------------------------------------------------

    judge = OllamaJudge(
        model=JUDGE_MODEL
    )

    # -------------------------------------------------------------------------
    # Configure generator metrics
    # -------------------------------------------------------------------------

    faithfulness_metric = FaithfulnessMetric(
        threshold=THRESHOLD,
        model=judge,
        include_reason=True,
        async_mode=False,
    )

    answer_relevancy_metric = AnswerRelevancyMetric(
        threshold=THRESHOLD,
        model=judge,
        include_reason=True,
        async_mode=False,
    )

    # -------------------------------------------------------------------------
    # Run evaluation
    # -------------------------------------------------------------------------

    logger.info("=" * 80)
    logger.info(
        f"RUNNING GENERATOR EVALUATION "
        f"({len(test_cases)} TEST CASES)"
    )
    logger.info("=" * 80)

    results = evaluate(
        test_cases=test_cases,
        metrics=[
            faithfulness_metric,
            answer_relevancy_metric,
        ],
        async_config=AsyncConfig(
            run_async=False
        ),
    )

    # -------------------------------------------------------------------------
    # Completion
    # -------------------------------------------------------------------------

    logger.info("=" * 80)
    logger.info("GENERATOR EVALUATION COMPLETED")
    logger.info("=" * 80)

    logger.info(
        f"Total test cases evaluated: {len(test_cases)}"
    )

    return results


# =============================================================================
# Entry Point
# =============================================================================

if __name__ == "__main__":
    main()