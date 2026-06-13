import os
import requests
import json
import re
from dotenv import load_dotenv

load_dotenv()


class LLMHandler:
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_TOKEN")
        self.api_url = os.getenv(
            "API_URL", "https://router.huggingface.co/v1/chat/completions"
        )
        self.model = os.getenv("MODEL_NAME", "deepseek-ai/DeepSeek-V3.2:novita")

        if not self.api_token:
            raise ValueError("HUGGINGFACE_TOKEN not set in .env")

    def generate(self, messages, max_tokens=4096, temperature=0.2):
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        try:
            response = requests.post(
                self.api_url, headers=headers, json=payload, timeout=120
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"ERROR: {str(e)}"

    def clean_json_response(self, response):
        """Robust JSON cleaning as per paper Sec IV.B.1"""
        # 1. Strip ```json blocks
        response = re.sub(r"```json\n?", "", response)
        response = re.sub(r"```\n?", "", response)

        # 2. Fix unquoted keys
        response = re.sub(r"(\w+)(?=\s*:)", r'"\1"', response)

        # 3. Add missing commas before }
        response = re.sub(r"(?<=\w)\s*(?=\})", ",", response)

        # 4. Extract JSON object
        start = response.find("{")
        end = response.rfind("}")
        if start != -1 and end != -1:
            response = response[start : end + 1]

        try:
            return json.loads(response)
        except:
            # Fallback: try to fix trailing commas
            response = re.sub(r",\s*}", "}", response)
            response = re.sub(r",\s*]", "]", response)
            try:
                return json.loads(response)
            except:
                return {"error": "JSON parse failed", "raw": response}

    def extract_code(self, text, target_lang="python"):
        """Extract code from markdown blocks"""
        pattern = rf"```{target_lang}\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()

        match = re.search(r"```\w*\n(.*?)```", text, re.DOTALL)
        if match:
            return match.group(1).strip()

        return text.strip()
