from pydantic import BaseModel, Field
from typing import Annotated, List, Optional
from .ollama_translator import OllamaTranslator


class TermsTableItem(BaseModel):
    src: str
    dst: str
    info: Optional[str] = None

    def to_prompt(self) -> str:
        return f"{self.src} -> {self.dst}" + (f" #{self.info}" if self.info else "")


class SakuraTranslator(OllamaTranslator):
    class Meta(OllamaTranslator.Meta):
        identifier = "sakura"
        description = "Sakura translator with sakura-14b (based on Ollama), prompt is built with terms_table."

    class Config(OllamaTranslator.Config):
        terms_table: Annotated[
            List[TermsTableItem], Field(description="terms table for translation")
        ] = []

    def __init__(self, cfg: Config) -> None:
        new_cfg = cfg.model_copy()
        new_cfg.prompt = self._build_sakura_prompt(new_cfg.terms_table)
        new_cfg.model = "crosery/sakura-14b-qwen2.5-v1.0-q6k"
        super().__init__(cfg)

    @staticmethod
    def _build_sakura_prompt(terms: List[TermsTableItem]) -> str:
        user_prompt = (
            "根据以下术语表（可以为空）：\n"
            + "\n".join([item.to_prompt() for item in terms])
            + "\n"
            + "将下面的日文文本根据对应关系和备注翻译成中文："
            + "{raw_text}"
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
        return super().translate(text)
