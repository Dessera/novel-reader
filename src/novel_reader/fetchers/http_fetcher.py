import requests
from pydantic import Field
from typing import Annotated, Dict, Optional

from .base_fetcher import BaseFetcher

from ..novel import NovelDocument


class HttpFetcher(BaseFetcher):
    class Meta(BaseFetcher.Meta):
        identifier = "http"

    class Config(BaseFetcher.Config):
        http_proxy: Annotated[
            Optional[str], Field(description="HTTP proxy address")
        ] = None
        https_proxy: Annotated[
            Optional[str], Field(description="HTTPS proxy address")
        ] = None

    def _build_proxies(self):
        proxies: Dict[str, str] = {}
        if self.params["http_proxy"] is not None:
            proxies["http"] = self.params["http_proxy"]
        if self.params["https_proxy"] is not None:
            proxies["https"] = self.params["https_proxy"]
        return proxies

    def _build_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:135.0) Gecko/20100101 Firefox/135.0"
        }

    def fetch(self, url: str):
        section = requests.get(
            url,
            headers=self._build_headers(),
            proxies=self._build_proxies(),
        ).text
        return NovelDocument(title="", sections=[section])
