from src.prompts import SCAM_CLASSIFICATION_PROMPT, EXPLAINER_PROMPT


def test_prompts_are_defined():
    assert "SCAM" in SCAM_CLASSIFICATION_PROMPT
    assert "red_flags" in SCAM_CLASSIFICATION_PROMPT
    assert "explain" in EXPLAINER_PROMPT.lower()
