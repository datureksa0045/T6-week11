from dataclasses import dataclass
from typing import List


@dataclass
class Comment:
    id: int
    post_id: int
    name: str
    email: str
    body: str


@dataclass
class Post:
    id: int
    title: str
    body: str
    author: str
    slug: str
    status: str
    comments: List[Comment] = None

    def __post_init__(self):
        if self.comments is None:
            self.comments = []
