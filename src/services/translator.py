import json
from pathlib import Path

def get_translation(lang: str) -> dict:
    try:
        with open(f"src/assets/translations/{lang}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback a inglés si no existe el idioma
        with open("src/assets/translations/en.json", "r", encoding="utf-8") as f:
            return json.load(f)
