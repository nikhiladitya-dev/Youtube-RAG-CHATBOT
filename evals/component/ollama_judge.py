import asyncio
import json

import ollama
from deepeval.models.base_model import DeepEvalBaseLLM


class OllamaJudge(DeepEvalBaseLLM):

    def __init__(self, model: str = "qwen3:4b"):
        self.model = model

    def load_model(self):
        return self.model

    def _clean_output(self, output: str) -> str:
        output = output.strip()

        if output.startswith("```json"):
            output = output[7:]

        elif output.startswith("```"):
            output = output[3:]

        if output.endswith("```"):
            output = output[:-3]

        return output.strip()

    def generate(self, prompt: str, schema=None):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        """
 You are an expert, impartial evaluator for a Retrieval-Augmented Generation (RAG) system.

Your task is to independently evaluate a generated answer across two distinct dimensions:

1. Faithfulness — groundedness in the retrieved context
2. Answer Relevancy — direct alignment with the user's query

### Input Data

- [User Query]&#58; {{query}}
- [Retrieved Context]&#58; {{context}}
- [Actual Answer]&#58; {{actual_answer}}

---

### Dimension 1: Faithfulness

Goal: Determine whether the factual claims in the Actual Answer are supported by the Retrieved Context.

Rules:

- Evaluate the Actual Answer against the Retrieved Context.
- Do NOT use outside knowledge.
- Do NOT use the expected answer to determine faithfulness.
- Paraphrasing that preserves meaning is fully acceptable.
- Additional information is acceptable when it is directly supported by the Retrieved Context.
- Do not penalize an answer simply because it contains more information than the expected answer.
- Evaluate each material factual claim independently.

Classify each claim as:

SUPPORTED:
The claim is directly stated or clearly entailed by the Retrieved Context.

UNSUPPORTED:
The claim is not supported by the Retrieved Context, even if it may be factually true in the real world.

CONTRADICTORY:
The claim directly conflicts with information in the Retrieved Context.

OVERGENERALIZED:
The claim is stronger, broader, or more absolute than the Retrieved Context supports.
For example, changing "sometimes" to "always" or "can" to "will".

Do not penalize timestamps, formatting, headings, or stylistic elements unless they contain a factual claim that conflicts with the context.

### Faithfulness Scoring

1.00:
All material factual claims are directly supported or clearly entailed by the Retrieved Context.

0.75–0.99:
Core claims are completely supported, with only very minor imprecision or wording differences and no meaningful unsupported, contradictory, or over-generalized claim.

0.40–0.74:
The answer is partially grounded but contains one or more meaningful unsupported or over-generalized claims while the primary conclusion remains supported.

0.01–0.39:
The answer contains substantial unsupported or contradictory information.

0.00:
The answer is entirely unsupported or directly contradicts the core information in the Retrieved Context.

IMPORTANT:
Before assigning a Faithfulness score below 0.70, identify the specific claim or claims that are UNSUPPORTED, CONTRADICTORY, or OVERGENERALIZED.

If all material factual claims are supported by the Retrieved Context, do not assign a Faithfulness score below 0.70.

---

### Dimension 2: Answer Relevancy

Goal: Determine how directly and completely the Actual Answer addresses the User Query.

Rules:

- Evaluate the Actual Answer against the User Query.
- Do NOT require the Actual Answer to match the Expected Answer word-for-word.
- Helpful elaboration is allowed and should not be penalized merely because of length.
- Additional information is acceptable when it directly helps answer the user's question.
- Penalize unrelated, distracting, or tangential information.
- Penalize answers that fail to address the core question.
- Penalize refusal when the Retrieved Context contains sufficient information to answer the query.

### Answer Relevancy Scoring

1.00:
Directly, clearly, and completely answers the User Query without irrelevant information.

0.75–0.99:
Directly answers the main query but contains minor non-essential detail or wordiness.

0.40–0.74:
Partially addresses the query, misses an important part, or contains substantial irrelevant information.

0.01–0.39:
Fails to answer the core question but touches on related topics.

0.00:
Completely off-topic, evasive, or answers an unrelated question.

IMPORTANT:
Before assigning an Answer Relevancy score below 0.70, identify the specific part of the User Query that was not answered or the specific irrelevant content that justifies the lower score.

---

### Evaluation Workflow

1. Extract the material factual claims from the Actual Answer.
2. Classify each claim against the Retrieved Context.
3. Determine Faithfulness reasoning.
4. Determine the Faithfulness score.
5. Determine whether the Actual Answer directly addresses the User Query.
6. Determine Answer Relevancy reasoning.
7. Determine the Answer Relevancy score.
8. Ensure that the reasoning and numerical scores are logically consistent.

### Output Format

Respond ONLY with a valid JSON object matching this schema:

{
  "claim_analysis": [
    {
      "claim": "<extracted claim>",
      "status": "SUPPORTED | UNSUPPORTED | CONTRADICTORY | OVERGENERALIZED",
      "citation_or_critique": "<supporting context or explanation>"
    }
  ],
  "faithfulness_reasoning": "<step-by-step rationale>",
  "faithfulness_score": <float between 0.00 and 1.00>,
  "relevancy_reasoning": "<step-by-step rationale>",
  "relevance_score": <float between 0.00 and 1.00>
}
                        """
                        
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            options={
                "temperature": 0,
            },
            think=False,
            format=schema.model_json_schema() if schema is not None else "",
        )

        output = response["message"]["content"]

        if not output:
            raise ValueError(
                f"Ollama returned empty output for model {self.model}"
            )

        output = self._clean_output(output)

        # DeepEval requires a Pydantic object when a schema is supplied.
        if schema is not None:

            try:
                parsed_output = json.loads(output)

            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Ollama returned invalid JSON:\n{output}"
                ) from exc

            # Some models may return a bare list when the schema
            # contains a single list field.
            if isinstance(parsed_output, list):

                schema_fields = schema.model_fields

                if len(schema_fields) == 1:
                    field_name = next(iter(schema_fields))

                    parsed_output = {
                        field_name: parsed_output
                    }

            return schema.model_validate(parsed_output)

        return output

    async def a_generate(self, prompt: str, schema=None):
        return await asyncio.to_thread(
            self.generate,
            prompt,
            schema,
        )

    def get_model_name(self):
        return f"Ollama/{self.model}"