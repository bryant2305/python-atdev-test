translations = {
    "es": {
        "subject": "Tu recibo de nómina",
        "body": "Hola, adjunto encontrarás tu recibo de nómina."
    },
    "en": {
        "subject": "Your payslip",
        "body": "Hi, please find your payslip attached."
    }
}

def get_translation(lang):
    return translations.get(lang, translations["es"])
