import time
import requests
import random
import urllib.parse as URL
from tqdm import tqdm
from requests.models import PreparedRequest
from pydantic import Field
from typing import Annotated, Any, Dict, Iterable, List, Optional

from ..exceptions import HttpFetcherException
from ..novel import NovelDocument, Novel

from .base_fetcher import BaseFetcher


class HttpFetcher(BaseFetcher):
    class Meta(BaseFetcher.Meta):
        identifier = "http"
        description = "Http fetcher"

    class Config(BaseFetcher.Config):
        http_proxy: Annotated[
            Optional[str], Field(description="HTTP proxy address")
        ] = None
        https_proxy: Annotated[
            Optional[str], Field(description="HTTPS proxy address")
        ] = None
        fetch_delay: Annotated[
            float,
            Field(
                description="Seconds to wait between requests, set to negative to use random delay"
            ),
        ] = -1
        random_upper_bound: Annotated[
            float, Field(description="Upper bound for random delay")
        ] = 4.0
        random_lower_bound: Annotated[
            float, Field(description="Lower bound for random delay")
        ] = 1.0

        fetch_progress: Annotated[
            bool,
            Field(description="Whether to show fetch progress"),
        ] = True

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

    def _get_fetch_deplay(self) -> float:
        fetch_delay: float = self.params.get("fetch_delay", -1)
        if fetch_delay < 0:
            random_upper_bound: float = self.params.get("random_upper_bound", 4.0)
            random_lower_bound: float = self.params.get("random_lower_bound", 1.0)

            return random.uniform(random_lower_bound, random_upper_bound)
        else:
            return fetch_delay

    def enumerate[T](
        self, it: Iterable[T], desc: Optional[str] = None, unit: str = "it"
    ) -> Iterable[T]:
        fetch_progress: bool = self.params.get("fetch_progress", True)
        if fetch_progress:
            return tqdm(it, desc=desc, unit=unit)
        else:
            return it

    def delay(self, sec: Optional[float] = None):
        if sec is not None and sec < 0:
            raise ValueError("Delay must be a positive integer")
        time.sleep(sec or self._get_fetch_deplay())

    def build_url(self, base: str, path: str = "", params: Dict[str, Any] = {}) -> str:
        url = URL.urljoin(base, path)
        req = PreparedRequest()
        req.prepare_url(url, params)  # type: ignore
        return req.url or url

    def fetch(self, src: str):
        resp = requests.get(
            src,
            headers=self._build_headers(),
            proxies=self._build_proxies(),
        )
        if resp.status_code != 200:
            raise HttpFetcherException(reason=resp.reason)
        return NovelDocument(title="", sections=[resp.text])

    def fetch_all(self, src: str) -> Novel:
        novel_meta = self.fetch_meta(src)
        self.delay()

        search_results = self.search(src)
        self.delay()

        docs: List[NovelDocument] = []
        for res in self.enumerate(search_results):
            doc = self.fetch(res)
            docs.append(doc)
            self.delay()

        return Novel(novel_meta, docs)
