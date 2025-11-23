import os
import requests
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class LatimerClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        endpoint: str = "https://api.latimer.ai/getCompletion",
    ):
        self.api_key = api_key or os.getenv("LATIMER_API_KEY")
        if not self.api_key:
            raise ValueError("LATIMER_API_KEY environment variable is required")
        self.endpoint = endpoint
        self.headers = {"Content-Type": "application/json"}

        
    def generate(
        self, prompt: str, system_prompt: Optional[str] = None, timeout: int = 30
    ) -> Optional[str]:
        """
        Generate text from a prompt using the Latimer API
        """
        payload = {
            "apiKey": self.api_key,
            "message": prompt,
            "model": "gpt-4o-mini",
            "additionalMessages": [
                {
                    "role": "user",
                    "content": system_prompt
                }
            ]
        }

        try:
            resp = requests.post(
                self.endpoint, json=payload, headers=self.headers, timeout=timeout
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"[LatimerClient] error: {e}")
            return None

