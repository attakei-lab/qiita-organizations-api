from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    """ページネーションデータ"""

    next: Optional[str] = None
    prev: Optional[str] = None
    pages: int
    current: int


class ResourceSet(Generic[T], BaseModel):
    """ページネーションされているリソースセット"""

    data: List[T]
    pagination: Optional[Pagination] = None


class Organization(BaseModel):
    id: str
    name: str
    description: str
