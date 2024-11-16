from typing import Annotated, List

from pydantic import BaseModel


class ChannelModel(BaseModel):
    id: int
    name: str


class NewsContentModel(BaseModel):
    media: List[tuple[str, str]]
    header: str
    text: str


class NewsModel(BaseModel):
    from_channel: Annotated[dict | None, ChannelModel] = None
    tag_id: int
    content: Annotated[dict, NewsContentModel]
