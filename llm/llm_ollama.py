from llm.llm_interface import LLMInterface
import requests, os, json

class LLMOllama(LLMInterface):
    def __init__(self):
        self.ollamaIP = os.getenv("OLLAMA_IP")
        self.llm_url = f"http://{self.ollamaIP}:11434/api/generate"
        self.model = "gemma-optimized:latest"
        
    def get_embedding(self):
        headers = {
            'Content-Type': 'application/json'
        }

        # self.model = "phi3:mini"

        data = {
            "model": self.model,
            "prompt":f"context:{context}\n rules: Don't directly mention the context, give short responses\n query:{query}",
            "stream": False
        }

        
        try:
            response = requests.post(self.llm_url, data=json.dumps(data), headers=headers)
            response.raise_for_status()     
            result = json.loads(response.text)['response']

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            result = "Error"

        
        return response

        
    def query(self, context="", query=""):
        headers = {
            'Content-Type': 'application/json'
        }

        # self.model = "phi3:mini"

        data = {
            "model": self.model,
            "prompt":f"context:{context}\n rules: Don't directly mention the context, give short responses\n query:{query}",
            "stream": False
        }

        try:
            response = requests.post(self.llm_url, data=json.dumps(data), headers=headers)
            response.raise_for_status()     
            result = json.loads(response.text)['response']

        except requests.exceptions.RequestException as e:
            print(f"Error connecting to Ollama: {e}")
            result = "Error"

        return result
