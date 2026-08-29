import os
import time
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from google import generativeai as genai

from src.config import DEFAULT_PARAMS, GEMINI_API_KEY, MODEL_NAME
from src.utils import sanitize_json_response

load_dotenv()


class GeminiInterface:
    def __init__(self, model_name: Optional[str] = None):
        self.api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
        self.model_name = model_name or MODEL_NAME
        self.model = None

        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(self.model_name)

    def generate(self, prompt: str, temperature: float = 0.2, max_tokens: int = 1024) -> str:
        """Call the Gemini API and return the model text response."""
        if not self.model:
            raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file or configure the environment.")

        for attempt in range(3):
            try:
                response = self.model.generate_content(
                    prompt,
                    generation_config={
                        "temperature": temperature,
                        "max_output_tokens": max_tokens,
                    },
                )
                if hasattr(response, "text") and response.text:
                    return response.text
                return ""
            except Exception as exc:
                if attempt == 2:
                    raise RuntimeError(f"Gemini API call failed: {exc}") from exc
                time.sleep(1)

    def generate_json(self, prompt: str) -> Dict[str, Any]:
        """Call Gemini and parse structured JSON output."""
        result = self.generate(prompt, temperature=DEFAULT_PARAMS["temperature"], max_tokens=DEFAULT_PARAMS["max_output_tokens"])
        return sanitize_json_response(result)
