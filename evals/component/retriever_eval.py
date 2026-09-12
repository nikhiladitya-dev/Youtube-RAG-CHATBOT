import json
from pathlib import Path

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import (ContextualPrecisionMetric,ContextualRecallMetric,)
from deepeval.test_case import LLMTestCase
from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService
from app.services.retrieval_service import RetrievalService
from evals.component.ollama_judge import OllamaJudge


# CONFIGURATION
PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLDEN_DATASET_PATH = (
    PROJECT_ROOT
    / "evals"
    / "datasets"
    / "golden_dataset.json"
)

VIDEO_ID = "8hly31xKli0"
TOP_K = 4
THRESHOLD = 0.7
JUDGE_MODEL = "qwen3:4b"


# LOAD GOLDEN DATASET

def load_goldens():
    with open(
        GOLDEN_DATASET_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


# INITIALIZE PRODUCTION RETRIEVER
def initialize_retriever():

    embedding_service = EmbeddingService()
    vectorstore_service = VectorStoreService(embedding_service=embedding_service)
    retriever = RetrievalService(vector_store_service=vectorstore_service)
    return retriever


# BUILD DEEPEVAL TEST CASES

def build_test_cases(
    retriever: RetrievalService,
):

    goldens = load_goldens()
    test_cases = []

    print(f"Found {len(goldens)} golden test cases.")

    for index, golden in enumerate(goldens,start=1,):

        question = golden["question"]
        ideal_answer = golden["ideal_answer"]
        print(f"Retrieving context "f"for test case {index}/{len(goldens)}...")

        # Use the actual production retriever
        retrieved_documents = retriever.retrieve(query=question,video_id=VIDEO_ID,k=TOP_K,)

        # Convert retrieved Documents into
        # DeepEval retrieval context
        retrieval_context = [
            document.page_content
            for document in retrieved_documents
        ]

        test_case = LLMTestCase(
            input=question,

            expected_output=ideal_answer,

            # Generator is intentionally not evaluated here.
            actual_output=(
                "Generator not evaluated "
                "in retriever evaluation."
            ),

            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

    return test_cases


# RUN RETRIEVER EVALUATION

def run():

    print("\n" + "=" * 70)
    print("YouTube RAG — Retriever Evaluation")
    print("=" * 70)

    print(f"\nGolden Dataset : {GOLDEN_DATASET_PATH}")
    print(f"Video ID       : {VIDEO_ID}")
    print(f"Top-K          : {TOP_K}")
    print(f"Threshold      : {THRESHOLD}")
    print(f"Judge Model    : Ollama / {JUDGE_MODEL}")

    # Initialize production retriever

    print("\nInitializing production retriever...\n")

    retriever = initialize_retriever()

    print("Production retriever initialized successfully.")

    # Build test cases

    print("\nLoading golden dataset ""and retrieving contexts...\n")

    test_cases = build_test_cases( retriever=retriever)

    print(f"\nSuccessfully built "f"{len(test_cases)} DeepEval test cases.")

    # Initialize local Ollama judge
    print(f"\nInitializing local evaluation judge: "f"{JUDGE_MODEL}...")

    judge = OllamaJudge(model=JUDGE_MODEL)

    print("Ollama judge initialized successfully.")

    metrics = [

        ContextualPrecisionMetric(
            threshold=THRESHOLD,
            model=judge,
            include_reason=False,
            async_mode=False,
        ),

        ContextualRecallMetric(
            threshold=THRESHOLD,
            model=judge,
            include_reason=False,
            async_mode=False,
        ),
    ]

    # --------------------------------------------------------
    # Run DeepEval
    # --------------------------------------------------------

    print("\n" + "=" * 70)
    print("Running Retriever Evaluation")
    print("=" * 70)

    print(
        "\nMetrics:"
        "\n  - Contextual Precision"
        "\n  - Contextual Recall"
    )

    print(
        f"\nEvaluation judge:"
        f"\n  - Ollama"
        f"\n  - {JUDGE_MODEL}"
    )

    print("\nRunning sequentially to avoid ""overloading the local model...\n")

    results = evaluate(test_cases=test_cases,metrics=metrics,
        hyperparameters={
            "retrieval_strategy": "MMR",
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "top_k": TOP_K,
            "video_id": VIDEO_ID,
            "golden_dataset": str(
                GOLDEN_DATASET_PATH
            ),
            "judge_model": f"Ollama/{JUDGE_MODEL}",
        },

        async_config=AsyncConfig(
            run_async=False
        ),
    )
    # Evaluation completed
    print("\n" + "=" * 70)
    print("Retriever Evaluation Completed")
    print("=" * 70)

    return results


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run()