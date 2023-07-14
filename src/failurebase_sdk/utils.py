"""Utils module."""

from dataclasses import dataclass, asdict


@dataclass
class TestSchema:
    """Stores test data."""

    uid: str
    file: str
    marks: list[str]

    def dump(self) -> dict:
        """Dumps schema to dict."""

        return asdict(self)


@dataclass
class FailureSchema:
    """Stores event data."""

    test: TestSchema
    message: str
    traceback: str
    timestamp: str

    def dump(self) -> dict:
        """Dumps schema to dict."""

        return asdict(self)
