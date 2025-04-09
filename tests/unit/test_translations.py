from src.services.translator import get_translation

def test_get_translation_en():
    translations = get_translation("en", "email")
    assert translations["email"]["subject"] == "Your Payroll Statement"

def test_get_translation_fallback():
    translations = get_translation("invalid-lang", "email")
    assert "subject" in translations["email"]
