from docx import Document

class Item:
    """Tree data structure.
    Each object is a node representing a block of text in the word document, and points to other nodes containing blocks that are below it in the 
    MS Word level hierachy.
    eg: The block of text containing a chapter name maybe 'Heading 2' level. Under it, there maybe 2 subchapters of 'Heading 3' level.
    Each subchapter will have blocks of 'normal' text under it, and maybe a couple of 'Heading 4' blocks, which also has more 'normal' blocks under it.

    Even though there is no hard-coded logical mapping of the tree in the word document itself, the get_document_tree() function in the read_doc.py file
    will infer this mapping based on the order of appearance of the text blocks in a word document.
    """
    def __init__(self, level: str, name: str = '', parent = None) -> None:
        self.level = level # i.e. MS Word Heading 2 or Heading 3 or Heading 4 or Normal
        self.name = name # the content of the paragraph (if a heading this would be the heading name, if level = Normal, this would be the paragraph content). In hindsight, 'block_text' would have been a better name. 
        self.contents: list[Item] = [] # list of all Items with a level below it (eg: if an item was of level = Heading 3, this list would contain all Heading 4 and Normal Items under it)
        self.parent: Item = parent # item above it in the hierachy (if any)
        self.list: tuple[int,int] = None # holds the 2 values (from the XML representation of the word doc) that indicates the list positioning (w:ilvl & w:numId)

    def __str__(self) -> str:
        string = ''
        if self.level == 'Heading 2': string += '\033[31m'
        if self.level == 'Heading 3': string += '\033[32m'
        if self.level == 'Heading 4': string += '\033[33m'
        string += self.name
        if self.level != 'Normal': string += '\033[0m'
        string += '\n'
        for subitem in self.contents:
            string += subitem.__str__()
            string += '\n'
        return string
    
    def get_jsonstring(self) -> str:
        # In hindsight, it would have been easier to convert the Item to a dictionary,
        # and then use the python json library.
        string = '{'
        string += '"Heading Level":'
        string += '"'
        string += self.level; string += '"'
        string += ','
        string += '"Text":'
        string += '"'
        string += self.name; string += '"'
        if len(self.contents) == 0:
            string += '}'
        else:
            string += ','
            string += '"Sub-contents":'
            string += '['
            for sub_content in self.contents:
                string += sub_content.get_jsonstring()
                string += ','
            string = string[:-1] # remove last comma
            string += ']'
            string += '}'
        return string
    
    def get_names_tree_dict(self):
        """Returns the names (block text) of self and its subitems as a dictionary, except for 'Normal' items.
        Useful if you want to craft something like a table of contents.
        """
        dict = {
            "Name": None,
            "Level": None,
            "Subitems": []
        }
        dict["Name"] = self.name
        dict["Level"] = self.level
        for subitem in self.contents:
            if subitem.level == "Normal": continue
            dict["Subitems"].append(subitem.get_names_tree_dict())
        return dict
    
    def get_leaves(self, leaf_level: str = 'Normal'):
        """Gets all leaf nodes (Item objects) as a list.
        You can specify what a leaf is, else it will go to the lowest level ('Normal')
        """
        leaves = []
        if self.level == leaf_level:
            return [self]
        for subitem in self.contents:
            leaves += subitem.get_leaves(leaf_level)
        return leaves


def get_document_tree(filepath: str, ignore_QnA = True) -> list[Item]:
    """Specialized to get what I want from the ATPL book.
    
    Uses python docx to read the .docx file from the given filepath.

    Returns a list of Items.
    Each Item is of level = Heading 2, i.e. a chapter
    
    And naturally each Item will contain all the Items below it in the hierachy.
    If ignore_QnA flag is True, Questions and Answers Heading 3 level Items are ignored.

    In this implementation, 'Normal' blocks under 'Heading 2' blocks have been ignored (as these are usually just tables of content).
    'Heading 5' blocks have been ignored as the book only has 5 instances of them, showing MCQ answers.
    """
    document = Document(filepath)
    paragraphs = document.paragraphs

    chapters: list[Item] = []
    current_heading_2: Item = None
    current_heading_3: Item = None
    current_heading_4: Item = None

    for paragraph in paragraphs:
        style = paragraph.style.name
        if style == 'Heading 2': 
            current_heading_2 = Item('Heading 2', paragraph.text)
            chapters.append(current_heading_2)
            current_heading_3 = None
            current_heading_4 = None
        if not current_heading_2: continue

        if style == 'Heading 3': 
            current_heading_3 = Item('Heading 3', paragraph.text, current_heading_2)
            current_heading_2.contents.append(current_heading_3)
            current_heading_4 = None

        if style == 'Heading 4': 
            current_heading_4 = Item('Heading 4', paragraph.text, current_heading_3)
            current_heading_3.contents.append(current_heading_4)
            # print('\033[31mheading4\033[0m')
            # print('XML:')
            # element = paragraph._element
            # print(element.xml)

        if style == 'Normal':
            if current_heading_3: # Check if this is a 'Questions' or 'Answers' subchapter. In retrospect, I could have moved the 'if ignore_QnA' line to the top.
                para_text = current_heading_3.name
                para_text = para_text.strip()
                para_text.replace('\n',''); para_text.replace('\r',''); para_text.replace('\t','')
                if ignore_QnA:
                    if para_text == 'Questions' or para_text == 'Answers': continue

            parent = current_heading_4
            if parent == None: parent = current_heading_3
            if parent == None: parent = current_heading_2

            # identify if this 'normal' block is a list
            ilvl = None; numId = None
            try:
                ilvl = paragraph._element.xpath('./w:pPr/w:numPr/w:ilvl')[0].val
                numId = paragraph._element.xpath('./w:pPr/w:numPr/w:numId')[0].val
            except IndexError: pass

            item = Item('Normal', paragraph.text, parent)
            if ilvl != None and numId != None: item.list = (ilvl,numId)
            if current_heading_4: 
                current_heading_4.contents.append(item)
                # print('XML:')
                # element = paragraph._element
                # print(element.xml)
            elif current_heading_3: current_heading_3.contents.append(item)

    return chapters

