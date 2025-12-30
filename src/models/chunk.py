from dataclasses import dataclass
from typing import Any


@dataclass
class Chunk:

    chapter: str
    """Name of the chapter"""

    subchapter: str
    """Name of the sub-chapter"""

    markdown: str
    """Text contents (preferrably in markdown format)"""

    bookname: str
    """The name of the book this chunk belongs to"""

    embedding: list[float] | None = None
    """Vector embedding of the markdown"""

    def get_metadata(self) -> dict[str, Any]:
        return {
            "chapter": self.chapter,
            "subchapter": self.subchapter,
            "bookname": self.bookname,
        }
    

            