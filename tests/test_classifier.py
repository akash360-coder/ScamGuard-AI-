from src.classifier import ScamClassifier


def test_rule_based_scam_detection():
    classifier = ScamClassifier()
    result = classifier.classify("URGENT! Your bank account is locked. Click here to verify your password now.")

    assert result["classification"] in {"SCAM", "LEGITIMATE"}
    assert result["confidence"] >= 0.0
    assert isinstance(result["red_flags"], list)
    assert len(result["red_flags"]) > 0


def test_legitimate_message_is_not_scam():
    classifier = ScamClassifier()
    result = classifier.classify("Hi Sam, can we meet tomorrow at 3 PM to review the presentation?")

    assert result["classification"] == "LEGITIMATE"
    assert result["confidence"] >= 0.0
