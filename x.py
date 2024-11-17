from docx import Document

class Item:
    def __init__(self, level: str, name: str = '') -> None:
        self.level = level
        self.name = name
        self.contents: list[Item] = []

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


def get_document_tree(filepath: str) -> list[Item]:
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
            current_heading_3 = Item('Heading 3', paragraph.text)
            current_heading_2.contents.append(current_heading_3)
            current_heading_4 = None

        if style == 'Heading 4': 
            current_heading_4 = Item('Heading 4', paragraph.text)
            current_heading_3.contents.append(current_heading_4)

        if style == 'Normal':
            if current_heading_3:
                para_text = current_heading_3.name
                para_text = para_text.strip()
                para_text.replace('\n',''); para_text.replace('\r',''); para_text.replace('\t','')
                if para_text == 'Questions' or para_text == 'Answers': continue

            item = Item('Normal', paragraph.text)
            if current_heading_4: current_heading_4.contents.append(item)
            elif current_heading_3: current_heading_3.contents.append(item)

    return chapters

