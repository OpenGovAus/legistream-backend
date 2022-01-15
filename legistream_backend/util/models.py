from dataclasses import dataclass


@dataclass
class StreamModel:
    url: str
    is_live: bool
    title: str
    thumb: str
