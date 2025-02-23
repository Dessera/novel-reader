import ollama
from pydantic import Field
from typing import Annotated
from .base_translator import BaseTranslator


class SakuraTranslator(BaseTranslator):
    class Meta(BaseTranslator.Meta):
        identifier = "sakura"

    class Config(BaseTranslator.Config):
        client_url: Annotated[str, Field(description="ollama client url")] = (
            "http://localhost:11434"
        )

    def __init__(self, cfg: Config) -> None:
        super().__init__(cfg)
        self._client = ollama.Client(cfg.client_url)

    def _build_prompt(self, text: str) -> str:
        user_prompt = (
            "根据以下术语表（可以为空）：\n"
            + ""
            + "\n"
            + "将下面的日文文本根据对应关系和备注翻译成中文："
            + text
        )
        prompt = (
            "<|im_start|>system\n你是一个轻小说翻译模型，可以流畅通顺地以日本轻小说的风格将日文翻译成简体中文，并联系上下文正确使用人称代词，不擅自添加原文中没有的代词。<|im_end|>\n"
            + "<|im_start|>user\n"
            + user_prompt
            + "<|im_end|>\n"
            + "<|im_start|>assistant\n"
        )
        return prompt

    def translate(self, text: str) -> str:
        return self._client.generate(
            model="crosery/sakura-14b-qwen2.5-v1.0-q6k", prompt=self._build_prompt(text)
        ).response
