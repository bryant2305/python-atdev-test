import json
from pathlib import Path

def get_translation(lang: str, template_type: str = 'email') -> dict:
    """Load translations from JSON files"""
    try:
        file_path = Path(f"src/assets/translations/{lang}.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # Fallback a inglés si no existe el archivo
        file_path = Path(f"src/assets/translations/en.json")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)