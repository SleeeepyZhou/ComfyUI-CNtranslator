import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class TranslatorShow:
    def __init__(self):
        pass

    CATEGORY = "utils"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input_text": ("STRING", {"default": "", "multiline": True})
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    OUTPUT_NODE = True
    FUNCTION = "transmit"

    def transmit(self, input_text):
        return input_text

class CNtranslator:
    def __init__(self):
        pass

    CATEGORY = "utils"

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "input": ("STRING", {"forceInput": True}),
                "CN2EN": ("BOOLEAN", {"default": True}),
                "out": ("STRING", {"default": "", "multiline": True})
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    OUTPUT_NODE = True
    FUNCTION = "translate"

    def translate(self, input, CN2EN, out):
        tags = re.split(r',|，', input)
        
        translations = [None] * len(tags)
        with ThreadPoolExecutor(max_workers=50) as executor:
            future_to_index = {executor.submit(ChineseTranslator.translate, tag, CN2EN): i for i, tag in enumerate(tags)}
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                translations[index] = future.result()
        ChineseTranslator.close_session()
        
        output = ",".join(filter(None, translations))
        out = output
        return (output,)
    
class ChineseTranslator:
    def __init__(self):
        self.client = requests.Session()

    def translate(self, text : str, c2e : bool):
        if not text:
            return None
        
        payload = {}
        if c2e:
            payload = {
                "appid": "105",
                "sgid": "zh-CN",
                "sbid": "zh-CN",
                "egid": "en",
                "ebid": "en",
                "content": text,
                "type": "2",
            }
        else:
            payload = {
                "appid": "105",
                "sgid": "en",
                "sbid": "en",
                "egid": "zh-CN",
                "ebid": "zh-CN",
                "content": text,
                "type": "2",
            }

        response = self.client.post("https://translate-api-fykz.xiangtatech.com/translation/webs/index", data=payload)
        if response.status_code == 200:
            json_data = response.json()
            by_value = json_data.get("by", "")
            if not by_value:
                return None
            return by_value
        return None

    def close_session(self):
        self.client.close()