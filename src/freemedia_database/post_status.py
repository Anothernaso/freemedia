from enum import Enum


class PostStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
