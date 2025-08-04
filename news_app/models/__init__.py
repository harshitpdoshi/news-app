from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class Feed:
    """Represents an RSS feed"""
    id: int
    url: str
    title: str
    description: str = ""
    last_updated: Optional[datetime] = None

@dataclass
class Article:
    """Represents an article from an RSS feed"""
    id: int
    feed_id: int
    title: str
    link: str
    summary: str = ""
    published: Optional[datetime] = None
    author: str = ""
    read: bool = False