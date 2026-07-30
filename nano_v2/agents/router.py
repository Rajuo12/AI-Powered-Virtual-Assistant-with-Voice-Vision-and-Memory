from nano_v2.agents.llm import LLMManager


class Router:
    def __init__(self):
        self.llm = LLMManager()

    def process(self, text: str):
        """
        Route every request to the LLM.
        Later we'll add tool routing.
        """
        return self.llm.chat(text)