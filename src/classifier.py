import json

from src.llm_interface import GeminiInterface
from src.prompts import EXPLAINER_PROMPT, SCAM_CLASSIFICATION_PROMPT


class ScamClassifier:
    def __init__(self):
        self.llm = GeminiInterface()

    def classify(self, text: str) -> dict:
        """Return structured classification output. Uses a fallback rule-based check if the LLM is unavailable."""
        if not text or not text.strip():
            return {
                "classification": "LEGITIMATE",
                "scam_type": "empty_input",
                "confidence": 0.0,
                "intent": "No intent detected",
                "red_flags": [],
                "reasoning": "No message provided for analysis.",
                "suspicious_phrases": [],
            }

        try:
            prompt = SCAM_CLASSIFICATION_PROMPT.format(user_input=text)
            result = self.llm.generate_json(prompt)
            validated = self._validate_response(result)
            if validated["classification"] == "SCAM":
                return validated
            return validated
        except Exception:
            return self._fallback_rule_based_classify(text)

    def explain(self, text: str, classification_result: dict) -> str:
        """Generate a human-friendly explanation."""
        prompt = EXPLAINER_PROMPT.format(user_input=text, analysis=json.dumps(classification_result, ensure_ascii=False))
        try:
            return self.llm.generate(prompt)
        except Exception:
            return self._default_explanation(classification_result)

    def _validate_response(self, response: dict) -> dict:
        defaults = {
            "classification": "LEGITIMATE",
            "scam_type": "unknown",
            "confidence": 0.5,
            "intent": "Not identified",
            "red_flags": [],
            "reasoning": "No reasoning provided.",
            "suspicious_phrases": [],
        }
        cleaned = dict(defaults)
        cleaned.update(response or {})
        cleaned["confidence"] = float(cleaned.get("confidence", 0.5))
        cleaned["red_flags"] = list(cleaned.get("red_flags", []))
        cleaned["suspicious_phrases"] = list(cleaned.get("suspicious_phrases", []))
        if cleaned["classification"] not in {"SCAM", "LEGITIMATE"}:
            cleaned["classification"] = "LEGITIMATE"
        return cleaned

    def _fallback_rule_based_classify(self, text: str) -> dict:
        lower = text.lower()
        red_flags = []

        suspicious_markers = {
            "urgent": ["urgent", "immediately", "asap"],
            "banking": ["bank", "verify account", "locked account", "suspended"],
            "payment": ["wire transfer", "gift card", "bitcoin", "cash app"],
            "credentials": ["password", "otp", "one time code", "verify your login"],
            "threat": ["legal action", "fine", "arrest", "suspension"],
        }

        for category, markers in suspicious_markers.items():
            if any(marker in lower for marker in markers):
                red_flags.append(category)

        is_scam = bool(red_flags) or any(word in lower for word in ["click here", "claim prize", "winner", "verify now", "urgent"])

        if is_scam:
            return {
                "classification": "SCAM",
                "scam_type": "phishing",
                "confidence": 0.9,
                "intent": "Steal credentials or money",
                "red_flags": red_flags or ["Urgent language and account verification request"],
                "reasoning": "The message uses urgency, pressure, and credential-seeking language that matches common scam patterns.",
                "suspicious_phrases": [phrase for phrase in ["urgent", "verify now", "password", "locked account"] if phrase in lower],
            }

        return {
            "classification": "LEGITIMATE",
            "scam_type": "none",
            "confidence": 0.85,
            "intent": "Routine communication",
            "red_flags": [],
            "reasoning": "The message appears to be a normal conversation without urgent scam indicators.",
            "suspicious_phrases": [],
        }

    def _default_explanation(self, classification_result: dict) -> str:
        if classification_result.get("classification") == "SCAM":
            return "This message contains common scam cues such as urgency, fear, or pressure to act immediately. These signals are often used to push victims into revealing credentials or sending money."
        return "This message looks like a normal, everyday communication and does not present obvious scam pressure, threats, or requests for sensitive information."
