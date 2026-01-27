# Amazon NOVA Client
import os
import json
from openai import AsyncOpenAI # Nova Model uses OpenAI's API Schema
from typing import Type
from pydantic import BaseModel, ValidationError
# use tenacity to retry when desired
from tenacity import AsyncRetrying, stop_after_attempt, wait_fixed, retry_if_exception_type

from .protocols import PydanticModel, TypedLLMProtocol, ProvidesProviderInfo
from .protocols import RateLimitProvider
import asyncio
from concurrent.futures import ThreadPoolExecutor

# helper to format Pydantic's JSON properties into a clean format ready for Nova Client
def format_json_schema(properties: dict) -> str:
    # Map JSON schema types to Python type names
        type_mapping = {
            "boolean": "bool",
            "string": "str", 
            "integer": "int",
            "number": "float",
            "array": "list",
            "object": "dict"
        }

        # Create clean format string
        format_lines = ["{"]
        for field, info in properties.items():
            json_type = info.get("type", "value")
            python_type = type_mapping.get(json_type, json_type)
            format_lines.append(f'  "{field}": {python_type}')
        format_lines.append("}")

        clean_format = "\n".join(format_lines)
        return clean_format
    
# Set up this client with API key during app initialization
# TODO: "strict" JSON/Pydantic output is only supported for Enterprise-level Nova LLM clients; set up manual validation to catch malformed JSON outputs before crashing Pydantic validation, or loosen validation.
# NOTE: The output schema must be enforced using the system prompt, so we automatically bake parsed Pydantic schema into the system prompt
class AsyncAmazonNovaTypedClient(TypedLLMProtocol, ProvidesProviderInfo):
    def __init__(
        self,
        model_name: str = "nova-2-lite-v1", # given from documentation, could be swapped depending on rate limits / pricing
        *,
        api_key: str | None = None,
        retry_attempts: int = 2,
        retry_wait: float = 0.1,
        retry_on: type[Exception] = ValidationError, # only retry when LLM fails to meet Pydantic validation
    ):
        # Create shared client in __init__ for FastAPI (ASGI)
        # FastAPI runs in a single event loop, so sharing the client is safe and efficient
        # This enables connection pooling and reduces overhead compared to creating a new client per request
        self.client = AsyncOpenAI(api_key=api_key, base_url="https://api.nova.amazon.com/v1") # Nova-compatible base url
        self.model_name = model_name
        # Provider metadata for reporting
        self.provider = RateLimitProvider.AWS
        self.model = model_name
        self.retryer = AsyncRetrying(
            stop=stop_after_attempt(retry_attempts),
            wait=wait_fixed(retry_wait),
            retry=retry_if_exception_type(retry_on),
            reraise=True,
        )

    async def acreate(
        self,
        response_model: Type[PydanticModel],
        system_prompt: str,
        user_prompt: str,
        **kwargs,
    ) -> PydanticModel:

        last_exception = None
        attempt_count = 0
        
        # Get schema from Pydantic model
        schema = response_model.model_json_schema()
        properties = schema.get("properties", {})
        # format into clean structure ready for Nova
        clean_format = format_json_schema(properties)

        # construct guided system prompt w/ JSON schema, then append to provided system prompt
        schema_guide_prompt = f"""
        You must respond with valid JSON only, in exactly this format:
        {clean_format}
        """
        guided_system_prompt = f"{system_prompt}\n\n{schema_guide_prompt}"

        async for attempt in self.retryer:
            attempt_count += 1
            with attempt: # let tenacity see context of each attempt instead of swallowing until the last
                try:
                    resp = await self.client.chat.completions.create(
                        model=self.model_name,
                        messages=[
                            {"role": "system", "content": guided_system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        response_format={"type": "json_object"}, # enforces JSON mode
                        **kwargs,
                    )

                    # Extract content from OpenAI response structure
                    content = resp.choices[0].message.content
                    if content and isinstance(content, str) and content.strip():
                        # Strip markdown code fences if present
                        content = content.strip()
                        if content.startswith("```"):
                            # Remove opening fence (```json or ````)
                            content = content.split("\n", 1)[1] if "\n" in content else content
                            # Remove closing fence
                            if content.endswith("```"):
                                content = content.rsplit("```", 1)[0]
                            content = content.strip()

                        # Manually validate the JSON string against the Pydantic model
                        return response_model.model_validate_json(content)

                    # Force a retryable failure when output is empty/invalid
                    raise ValueError("LLM response was empty or not parseable to JSON.")
                
                except ValidationError as e:
                    last_exception = e
                    # Let tenacity handle retry/terminal re-raise
                    raise
                except Exception as e:
                    last_exception = e
                    # Let tenacity handle retry/terminal re-raise
                    raise
        
        # This should never be reached, but if it is, provide better error info
        # NOTE: **IMPORTANT** If we get here, the loop ran zero times (misconfigured retryer) or exited cleanly without return.
        raise RuntimeError(
            f"acreate() reached unexpected fallthrough after {attempt_count} attempts; "
            f"retryer likely yielded no final exception and no success. last_exc={type(last_exception).__name__ if last_exception else None}"
        )
