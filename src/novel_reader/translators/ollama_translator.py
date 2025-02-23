import ollama
from pydantic import Field
from typing import Annotated

from .base_translator import BaseTranslator


class OllamaTranslator(BaseTranslator):
    class Meta(BaseTranslator.Meta):
        identifier = "ollama"
        description = "Ollama translator"

    class Config(BaseTranslator.Config):
        client_url: Annotated[str, Field(description="Ollama client url")] = (
            "http://localhost:11434"
        )
        model: Annotated[str, Field(description="Ollama model")] = "llama3.2"
        prompt: Annotated[
            str,
            Field(description="Prompt for translation, use {raw_text} as placeholder"),
        ] = "{raw_text}"

    def __init__(self, cfg: Config) -> None:
        super().__init__(cfg)
        self._client = ollama.Client(cfg.client_url)

    def _build_prompt(self, text: str) -> str:
        prompt: str = self.params["prompt"]
        return prompt.format(raw_text=text)

    def translate(self, text: str) -> str:
        model: str = self.params["model"]
        return self._client.generate(model, self._build_prompt(text)).response
