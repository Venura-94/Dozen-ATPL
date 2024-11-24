from docx import Document

class Item:
    def __init__(self, level: str, name: str = '', parent = None) -> None:
        self.level = level # i.e. MS Word Heading 2 or Heading 3 or Heading 4 or Normal
        self.name = name # the content of the paragraph (if a heading this would be the heading name, if level = Normal, this would be the paragraph content)
        self.contents: list[Item] = [] # list of all Items with a level below it (eg: if an item was of level = Heading 3, this list would contain all Heading 4 and Normal Items under it)
        self.parent: Item = parent # item above it in the hieracy (if any)

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
        """Returns self and its subitems as a dictionary, except for 'Normal' items.
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
    
    def get_leaves(self):
        leaves = []
        if self.level == 'Normal':
            return [self]
        for subitem in self.contents:
            leaves += subitem.get_leaves()
        return leaves


def get_document_tree(filepath: str) -> list[Item]:
    """Uses python docx to read the .docx file from the given filepath.
    Returns a list of Items.
    Each Item is of level = Heading 2, i.e. a chapter
    And naturally each Item will contain all the Items below it in the hierachy.
    Questions and Answers Heading 3 level Items are ignored.
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

        if style == 'Normal':
            if current_heading_3:
                para_text = current_heading_3.name
                para_text = para_text.strip()
                para_text.replace('\n',''); para_text.replace('\r',''); para_text.replace('\t','')
                if para_text == 'Questions' or para_text == 'Answers': continue

            parent = current_heading_4
            if parent == None: parent = current_heading_3
            if parent == None: parent = current_heading_2

            item = Item('Normal', paragraph.text, parent)
            if current_heading_4: current_heading_4.contents.append(item)
            elif current_heading_3: current_heading_3.contents.append(item)

    return chapters

