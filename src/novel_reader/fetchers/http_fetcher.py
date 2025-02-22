from typing import Dict, Optional
import requests

from .base_fetcher import BaseFetcher

from ..novel import NovelDocument


class HttpFetcher(BaseFetcher):
    IDENTIFIER = "http"

    class Config(BaseFetcher.Config):
        http_proxy: Optional[str] = None
        https_proxy: Optional[str] = None

    def __init__(self, cfg: Config):
        super().__init__(cfg)
        self._http_proxy = cfg.http_proxy
        self._https_proxy = cfg.https_proxy

    def _build_proxies(self):
        proxies: Dict[str, str] = {}
        if self._http_proxy is not None:
            proxies["http"] = self._http_proxy
        if self._https_proxy is not None:
            proxies["https"] = self._https_proxy
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
