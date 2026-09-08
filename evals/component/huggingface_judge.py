import asyncio
import json

from deepeval.models.base_model import DeepEvalBaseLLM
from huggingface_hub import InferenceClient


class HuggingFaceJudge(DeepEvalBaseLLM):

    def __init__(
        self,
        model: str,
        api_token: str,
    ):
        self.model = model

        self.client = InferenceClient(
            model=model,
            token=api_token,
        )


    def load_model(self):
        return self.client


    def _build_messages(
        self,
        prompt: str,
    ):

        return [
            {
                "role": "system",
                "content": (
                    "You are an evaluation model. "
                    "Follow the instructions exactly. "
                    "When structured JSON is requested, return ONLY valid JSON. "
                    "Do not include markdown fences or explanations outside the JSON."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ]


    def _parse_output(
        self,
        output: str,
        schema=None,
    ):

        if output is None:
            raise ValueError(
                "Hugging Face model returned empty content."
            )

        output = output.strip()

        # Remove markdown fences
        if output.startswith("```json"):
            output = output[7:]

        elif output.startswith("```"):
            output = output[3:]

        if output.endswith("```"):
            output = output[:-3]

        output = output.strip()

        if schema is not None:

            parsed_output = json.loads(
                output
            )

            # Normalize a bare list into the object structure
            # expected by DeepEval's Pydantic schema.
            if isinstance(parsed_output, list):

                schema_fields = schema.model_fields

                if len(schema_fields) == 1:

                    field_name = next(
                        iter(schema_fields)
                    )

                    parsed_output = {
                        field_name: parsed_output
                    }

            return schema.model_validate(
                parsed_output
            )

        return output

    def generate(
        self,
        prompt: str,
        schema=None,
    ):

        response = self.client.chat_completion(
            messages=self._build_messages(
                prompt
            ),
            temperature=0,
            max_tokens=2048,
        )

        output = (
            response
            .choices[0]
            .message
            .content
        )

        return self._parse_output(
            output=output,
            schema=schema,
        )


    async def a_generate(
        self,
        prompt: str,
        schema=None,
    ):

        response = await asyncio.to_thread(
            self.client.chat_completion,
            messages=self._build_messages(
                prompt
            ),
            temperature=0,
            max_tokens=2048,
        )

        output = (
            response
            .choices[0]
            .message
            .content
        )

        return self._parse_output(
            output=output,
            schema=schema,
        )


    def get_model_name(self):

        return self.model