from deepeval.metrics import AnswerRelevancyMetric
from deepeval.test_case import LLMTestCase


test_case = LLMTestCase(
    input="What is Python?",
    actual_output="Python is a programming language."
)

metric = AnswerRelevancyMetric(
    threshold=0.5,
    include_reason=True
)

metric.measure(test_case)

print("Score:", metric.score)
print("Reason:", metric.reason)