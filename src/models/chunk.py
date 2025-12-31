from dataclasses import dataclass
from typing import Any


@dataclass
class Chunk:
    """
    A single chunk for the RAG system.
    In the context of ATPL textbooks, I decided that a single chunk would be a subchapter in the textbook.
    This works well with the textbook:
    - it has an appropriate length
    - each subchapter tends to cover an independed topic, so chunk overlap is not that important
    - it's logical chunking for the ATPL student as well
    """

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
        """Get a dictionary with the chapter, subchapter and bookname as keys
        """
        return {
            "chapter": self.chapter,
            "subchapter": self.subchapter,
            "bookname": self.bookname,
        }
    

            