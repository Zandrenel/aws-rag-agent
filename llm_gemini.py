from llm_interface import LLMInterface
import requests, os, json

class LLMGemini(LLMInterface):
    def __init__(self):
        self.geminiAPIKey = os.getenv("GEMINI_API_KEY")
        self.llm_url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent'

    def query(self, context="", query=""):
        
        headers = {
            'x-goog-api-key':self.geminiAPIKey,
            'Content-Type': 'application/json'
        }

        data = {
            "contents":[
                {"parts":[
                    {"text":f"context:{context}\n rules: Don't directly mention the context, give short responses\n query:{query}"}
                ]}
            ]
        }
        
        postreq = requests.post(self.llm_url, data=json.dumps(data), headers=headers)

        return json.loads(postreq.text)["candidates"][0]["content"]["parts"][0]["text"]
