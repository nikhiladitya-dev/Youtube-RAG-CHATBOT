from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase

from evals.component.ollama_judge import OllamaJudge


# Initialize local evaluation judge
judge = OllamaJudge(model="qwen3:4b")


# Test case
test_case = LLMTestCase(
    input="What is Python?",
    actual_output="Python is a programming language."
)


# Evaluation metric
metric = AnswerRelevancyMetric(
    threshold=0.5,
    model=judge,
    include_reason=True,
    async_mode=False,
)


# Run evaluation
results = evaluate(
    test_cases=[test_case],
    metrics=[metric],
    async_config=AsyncConfig(run_async=False),
)

print("\nEvaluation completed.")
print(results)