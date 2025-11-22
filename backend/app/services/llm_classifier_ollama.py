import httpx
from app.core.config import settings

class LLMClassifierOllama:
    def __init__(self):
        self.base_url = settings.OLLAMA_HOST

    async def classify_lines(self, lines: list):
        # TODO: Implémenter l'appel à Ollama
        pass
