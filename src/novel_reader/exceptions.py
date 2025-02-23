from typing import Optional


class BaseReaderException(Exception):
    pass


class FactoryException(BaseReaderException):
    pass


class ModuleSearchException(FactoryException):
    TEMPLATE = "Unable to find objects in module {mod} ({package}): {reason}"

    def __init__(
        self, mod: str, package: Optional[str] = None, reason: Optional[str] = None
    ):
        self.mod = mod
        self.package = package or "Unknown package"
        self.reason = reason or "Unknown reason"

        super().__init__(
            self.TEMPLATE.format(mod=self.mod, package=self.package, reason=self.reason)
        )


class ObjectCreationException(FactoryException):
    TEMPLATE = "Unable to create {name} {identifier}: {reason}"

    def __init__(self, name: str, identifier: str, reason: Optional[str] = None):
        self.name = name
        self.identifier = identifier
        self.reason = reason or "Unknown reason"

        super().__init__(
            self.TEMPLATE.format(
                name=self.name, identifier=self.identifier, reason=self.reason
            )
        )


class FetcherException(BaseReaderException):
    pass


class HttpFetcherException(FetcherException):
    TEMPLATE = "HTTP fetcher error: {reason}"

    def __init__(self, reason: Optional[str] = None):
        self.reason = reason or "Unknown reason"

        super().__init__(self.TEMPLATE.format(reason=self.reason))
