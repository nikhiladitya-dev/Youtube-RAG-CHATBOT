import json
from pathlib import Path
from deepeval import evaluate
from deepeval.metrics import (
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)
from deepeval.test_case import LLMTestCase

from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService
from app.services.retrieval_service import RetrievalService

from evals.component.huggingface_judge import HuggingFaceJudge
from app.core.config import settings

# CONFIGURATION
PROJECT_ROOT = Path(__file__).resolve().parents[2]

GOLDEN_DATASET_PATH = (PROJECT_ROOT/ "evals"/ "datasets"/ "golden_dataset.json")
VIDEO_ID = "8hly31xKli0"
TOP_K = 4
THRESHOLD = 0.7


# LOAD GOLDEN DATASET
def load_goldens():

    with open(GOLDEN_DATASET_PATH,"r",
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

def build_test_cases(retriever: RetrievalService,):

    goldens = load_goldens()
    test_cases = []

    for golden in goldens:

        question = golden["question"]
        ideal_answer = golden["ideal_answer"]
        retrieved_documents = retriever.retrieve(
            query=question,
            video_id=VIDEO_ID,
            k=TOP_K,
        )

        retrieval_context = [
            document.page_content
            for document in retrieved_documents
        ]

        test_case = LLMTestCase(
            input=question,
            expected_output=ideal_answer,
            actual_output="Generator not evaluated in retriever evaluation.",
            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

    return test_cases


# RUN RETRIEVER EVALUATION

def run():

    print("\nInitializing production retriever...\n")

    retriever = initialize_retriever()

    print("\nLoading golden dataset and retrieving contexts...\n")

    test_cases = build_test_cases(
        retriever=retriever
    )

    JUDGE_MODEL = HuggingFaceJudge(
        model="Qwen/Qwen3-4B-Instruct-2507",
        api_token=settings.HF_TOKEN,
    )

    metrics = [

        ContextualPrecisionMetric(
            threshold=THRESHOLD,
            model = JUDGE_MODEL,
            include_reason=False,
            async_mode=False,
        ),

         ContextualRecallMetric(
            threshold=0.7,
            model=JUDGE_MODEL,
            include_reason=False,
            async_mode=False,
        ),

        
    ]

    print("\nRunning retriever evaluation...\n")

    results = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        hyperparameters={
            "retrieval_strategy": "MMR",
            "embedding_model": "BAAI/bge-small-en-v1.5",
            "top_k": TOP_K,
            "video_id": VIDEO_ID,
            "golden_dataset": str(
                GOLDEN_DATASET_PATH
            ),
        },
    
    )

    return results


if __name__ == "__main__":

    run()