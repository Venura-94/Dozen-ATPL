from typing import Any


class MSWordTextBlock:
    """
    An object that represents a block of text in a word document.

    By 'block of text' we mean a 'docx paragraph' (see https://python-docx.readthedocs.io/en/latest/user/quickstart.html#adding-a-paragraph). 'docx paragraphs' are
    a fundamental structure in a word document. Text paragraphs and headings are call considered 'docx paragraphs'.

    The level, text_content and list_positioning attributes directly represent elements from a 'docx paragraph'.

    Additionally, by using the parent_block and child_blocks attributes that point to other `MSWordTextBlock` objects, we can maintain a 'tree' of the word document.
    eg: 
        The block of text containing a chapter name maybe 'Heading 2' level. Under it, there maybe 2 subchapters of 'Heading 3' level.
        Each subchapter will have blocks of 'normal' text under it, and maybe a couple of 'Heading 4' blocks, which also has more 'normal' blocks under it.

    Even though there is no hard-coded logical mapping of the tree in the word document itself, we can use `MSWordTextBlock` objects pointing to each other to create one by parsing a word document.

    
    Attributes:
        level (str): The MS Word style of this particular text block. e.g.: 'Heading 2', 'Heading 3', 'Heading 4', 'Normal'
        text_content (str): The text content of this text block. (if a heading this would be the heading name, if level = Normal, this would be the paragraph content). 
        child_blocks (list[MSWordTextBlock]): list of all Items with a level below it (eg: if an item was of level = Heading 3, this list would contain all Heading 4 and Normal Items under it). Initialized as a blank list.
        parent_block (MSWordTextBlock): block above this one in the hieracy (if any) (Defaults to None)
        list_positioning (tuple[int,int]): If this block is also a MS Word list, this stores the following attributes indicating list positioning from the word xml (w:ilvl & w:numId)
    """

    def __init__(self, level: str, text_content: str = '', parent_block = None) -> None:
        self.level = level
        self.text_content = text_content
        self.child_blocks: list[MSWordTextBlock] = []
        self.parent_block: MSWordTextBlock = parent_block
        self.list_positioning: tuple[int,int] = None # holds the 2 values (from the XML representation of the word doc) that indicates the list positioning (w:ilvl & w:numId)

    def __str__(self) -> str:
        string = ''
        if self.level == 'Heading 2': string += '\033[31m'
        if self.level == 'Heading 3': string += '\033[32m'
        if self.level == 'Heading 4': string += '\033[33m'
        string += self.text_content
        if self.level != 'Normal': string += '\033[0m'
        string += '\n'
        for subitem in self.child_blocks:
            string += subitem.__str__()
            string += '\n'
        return string
    
    def as_dict(self, exclude_parent_block = True) -> dict[str, Any]:
        child_block_dicts = []
        for block in self.child_blocks:
            child_block_dicts.append(block.as_dict())

        dictionary = {
            "level": self.level,
            "text_content": self.text_content,
            "child_blocks": child_block_dicts,
            "list_positioning": self.list_positioning # the tuple will be automatically casted to a list (json only knows list, not tuple)
        }

        if not exclude_parent_block:
            dictionary["parent_block"] = self.parent_block.as_dict()

        return dictionary

    
    def get_table_of_contents(self) -> dict[str, Any]:
        """Similar to `as_dict` method in that a dictionary/nested dictionary is returned, but text blocks of level == 'Normal' are omitted. 
        The result is a dictionary structure representing a table of contents.
        """
        if self.level == 'Normal': return {}

        child_block_dicts = []
        for block in self.child_blocks:
            if block.level == "Normal": continue
            child_block_dicts.append(block.as_dict())

        dict = {
            "text_content": self.text_content,
            "level": self.level,
            "child_blocks": child_block_dicts,
        }

        return dict
    
    def get_leaves(self, leaf_level: str = 'Normal') -> list['MSWordTextBlock']:
        """Gets all child_blocks of the specified level.

        Note: Get the blocks at the specified level, not above it and not ones below it either.
        """
        leaves = []
        if self.level == leaf_level:
            return [self]
        for subitem in self.child_blocks:
            leaves += subitem.get_leaves(leaf_level)
        return leaves