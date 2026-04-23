from llm.llm_gemini import LLMGemini
from llm.llm_ollama import LLMOllama

class LLMFactory:
    def __init__(self):
        pass

    def gemini(self):
        return LLMGemini()
    
    def ollama(self):
        return LLMOllama()
