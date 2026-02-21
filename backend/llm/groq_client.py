"""
AI Travel Guardian+ — Groq LLM Client
Wrapper for Groq API with retry logic and streaming support.
"""

import time
import json
from typing import AsyncGenerator, Optional, List, Dict
from groq import Groq


class GroqLLMClient:
    """Groq API client with retry logic for both streaming and non-streaming calls."""

    def __init__(self, api_key: str, model: str = "llama3-8b-8192",
                 smart_model: str = "mixtral-8x7b-32768",
                 max_retries: int = 3, retry_delay: int = 2):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.fast_model = model
        self.smart_model = smart_model
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def chat(self, messages: List[Dict], model: str = None,
             temperature: float = 0.3, max_tokens: int = 1500) -> str:
        """Non-streaming chat completion with retry logic."""
        use_model = model or self.smart_model

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=use_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait = self.retry_delay * (2 ** attempt)
                    time.sleep(wait)
                else:
                    raise RuntimeError(f"Groq API failed after {self.max_retries} retries: {e}")

    def chat_json(self, messages: List[Dict], model: str = None,
                  temperature: float = 0.1, max_tokens: int = 2000) -> dict:
        """Chat completion that parses JSON response."""
        raw = self.chat(messages, model=model, temperature=temperature, max_tokens=max_tokens)
        # Try to extract JSON from response
        raw = raw.strip()
        if raw.startswith("```json"):
            raw = raw[7:]
        if raw.startswith("```"):
            raw = raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            # Try to find JSON within the text
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(raw[start:end])
                except json.JSONDecodeError:
                    pass
            # Try array
            start = raw.find("[")
            end = raw.rfind("]") + 1
            if start >= 0 and end > start:
                try:
                    return json.loads(raw[start:end])
                except json.JSONDecodeError:
                    pass
            return {"error": "Failed to parse JSON", "raw": raw[:500]}

    def stream_chat(self, messages: List[Dict], model: str = None,
                    temperature: float = 0.3, max_tokens: int = 1500):
        """Streaming chat completion (synchronous generator)."""
        use_model = model or self.smart_model

        for attempt in range(self.max_retries):
            try:
                stream = self.client.chat.completions.create(
                    model=use_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    stream=True,
                )
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                return
            except Exception as e:
                if attempt < self.max_retries - 1:
                    wait = self.retry_delay * (2 ** attempt)
                    time.sleep(wait)
                else:
                    yield f"\n[Error: LLM service unavailable after {self.max_retries} retries]"

    def test_connection(self) -> bool:
        """Test if Groq API is reachable."""
        try:
            response = self.client.chat.completions.create(
                model=self.fast_model,
                messages=[{"role": "user", "content": "Say 'ok'"}],
                max_tokens=5,
            )
            return bool(response.choices[0].message.content)
        except Exception:
            return False
