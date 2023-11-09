from enum import Enum
from typing import List, Optional, Any


class ContentType:
    POST_TITLE = 0
    POST_BODY = 1
    POST_LINK = 2
    COMMENT = 3


class Content:
    community: str
    content: str
    actor_id: str
    link_to_content: str
    type: ContentType

    def __init__(self, community: str, content: str, actor_id: str, link_to_content: str, type: ContentType):
        self.community = community
        self.content = content
        self.actor_id = actor_id
        self.link_to_content = link_to_content
        self.type = type


class ContentResult:
    flags: List[str]
    extras: Optional[Any]
    was_deleted: bool

    def __init__(self, flags: List[str], extras: Optional[Any], was_deleted: bool = False):
        self.flags = flags
        self.extras = extras
        self.was_deleted = was_deleted

    @staticmethod
    def nothing():
        return ContentResult([], None)


class Outcome(Enum):
    POSITIVE = 0
    NEGATIVE = 1
    OTHER = 2
