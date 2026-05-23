import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class PolicyAnalyzer:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment. Add it to .env.")

        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self):
        prompt_path = os.path.join(os.path.dirname(__file__), "docs", "system_prompt.md")
        try:
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return self._default_system_prompt()

    @staticmethod
    def _default_system_prompt():
        return """
You are an expert policy analyst specializing in educational data systems and charter school governance.
Your job is to parse policy updates and extract actionable insights for dashboard developers.
Always output valid JSON with the following fields:
{
  "rule_summary": "...",
  "grade_levels": [...],
  "affected_metrics": [...],
  "business_logic_summary": "...",
  "suggested_sql_update": "...",
  "ambiguities": [...],
  "confidence": "high|medium|low",
  "human_review_required": true
}
"""

    def analyze_policy(self, policy_text: str) -> dict:
        if not policy_text.strip():
            raise ValueError("Policy text cannot be empty.")

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": policy_text},
            ],
            temperature=0.2,
            max_tokens=1000,
        )

        choice = response.choices[0]
        text = getattr(choice.message, "content", None)
        if text is None:
            text = choice["message"]["content"]

        try:
            return json.loads(text)
        except json.JSONDecodeError as exc:
            raise ValueError(
                "AI response was not valid JSON. Check the system prompt or model output."
            ) from exc