from .translator import CNtranslator, TranslatorShow

NODE_CLASS_MAPPINGS = {
    "CNtranslator": CNtranslator, 
    "TextShow" : TranslatorShow,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CNtranslator": "🇨🇳 Translator",
}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']