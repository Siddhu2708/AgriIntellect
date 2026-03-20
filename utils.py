import json
import os

# Mapping of language names to Sarvam AI language codes
LANGUAGES_MAP = {
    "English": "en-IN", "Hindi": "hi-IN", "Marathi": "mr-IN", "Tamil": "ta-IN",
    "Telugu": "te-IN", "Kannada": "kn-IN", "Malayalam": "ml-IN", "Gujarati": "gu-IN",
    "Punjabi": "pa-IN", "Bengali": "bn-IN", "Odia": "or-IN", "Urdu": "ur-IN",
    "Assamese": "as-IN", "Nepali": "ne-IN", "Konkani": "kok-IN", "Maithili": "mai-IN",
    "Sindhi": "sd-IN", "Sanskrit": "sa-IN", "Santali": "sat-IN", "Bodo": "brx-IN",
    "Dogri": "doi-IN", "Kashmiri": "ks-IN", "Manipuri": "mni-IN"
}

def load_config():
    """Load API keys and other identifiers from config.json."""
    working_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(working_dir, "config.json")
    try:
        with open(config_path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def translate_text(sarvam_client, text, target_lang_name):
    """
    Translate text using Sarvam AI. 
    If target is English or an error occurs, returns original text.
    """
    if target_lang_name == "English":
        return text
    
    target_code = LANGUAGES_MAP.get(target_lang_name, "en-IN")
    try:
        response = sarvam_client.text.translate(
            input=text,
            source_language_code="en-IN",
            target_language_code=target_code,
            speaker_gender="Male",
            mode="formal",
            model="mayura:v1"
        )
        if hasattr(response, 'translated_text'):
            return response.translated_text
        return response
    except Exception:
        return text
