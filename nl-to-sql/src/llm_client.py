import json
import os
import anthropic
from .config import ANTHROPIC_MODEL


class ClaudeClient:
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            raise ValueError('ANTHROPIC_API_KEY is not configured.')
        self.client = anthropic.Anthropic(api_key=api_key)

    def generate(self, prompt: str, max_tokens: int = 1200) -> str:
        response = self.client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=max_tokens,
            temperature=0,
            messages=[{'role': 'user', 'content': prompt}],
        )
        return ''.join(block.text for block in response.content if hasattr(block, 'text')).strip()

    def classify_intent(self, prompt: str) -> dict:
        text = self.generate(prompt, max_tokens=200)
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {'intent': 'UNKNOWN', 'confidence': 0.0}
