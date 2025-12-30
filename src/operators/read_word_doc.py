from docx import Document

from src.models.msword_text_block import MSWordTextBlock


def get_document_tree(filepath: str, ignore_QnA = True) -> list[MSWordTextBlock]:
    """
    A function to extract text blocks in a tree structure from the filepath. This function is specialized to get the data we need from the ATPL textbook.

    In an ATPL textbook, the main chapter headings are at level 'Heading 2', and subchapters are at level 'Heading 3'.
    Because of the way this function works, we end up extracting only the data we need.
    - things between 'Heading 2' (chapter heading) and 'Heading 3' (sub-chapter heading) are ignored (things like tables of contents, could not find anything important).
    - but every single thing under a sub-chapter heading are extracted
        - e.g. in book 8 -> chapter '1 Basic Concepts' -> sub-chapter 'The Five Elements of Safety Culture', there is normal text under this sub-chapter, followed by a 'Heading 4' level,
        followed by more normal text and so on. All this data is captured.
    - 'Heading 5' blocks have been ignored as the book only has 5 instances of them, showing MCQ answers.
    - If sub chapter name is 'Questions' or 'Answers', it is ignored (if ignore_QnA argument is True), as these refer to MCQ QnAs at the end of chapters in the text book.
    - However does include the last chapter which contains a specimen exam.
    - Note that this will still return chapter 18 onwards which has specimen questions onwards.
    
    Uses python docx to read the .docx file from the given filepath.
    
    And naturally each Item will contain all the Items below it in the hierachy.
    If ignore_QnA flag is True, Questions and Answers Heading 3 level Items are ignored.

    Args:
        filepath (str): filepath to the word document of the ATPL text book
        ignore_QnA (bool): Defaults to True. Instructs function to ignore MCQ QnA chapter.

    Returns:
        list[MSWordTextBlock]: Tree. Each MSWordTextBlock is of level = Heading 2, i.e. a chapter. Each such MSWordTextBlock will contain the children belonging to it.
    """
    document = Document(filepath)
    paragraphs = document.paragraphs

    chapters: list[MSWordTextBlock] = []
    current_heading_2: MSWordTextBlock = None
    current_heading_3: MSWordTextBlock = None
    current_heading_4: MSWordTextBlock = None

    for paragraph in paragraphs:
        style = paragraph.style.name
        if style == 'Heading 2': 
            current_heading_2 = MSWordTextBlock('Heading 2', paragraph.text)
            chapters.append(current_heading_2)
            current_heading_3 = None
            current_heading_4 = None
        if not current_heading_2: continue

        if style == 'Heading 3': 
            current_heading_3 = MSWordTextBlock('Heading 3', paragraph.text, current_heading_2)
            current_heading_2.child_blocks.append(current_heading_3)
            current_heading_4 = None

        if style == 'Heading 4': 
            current_heading_4 = MSWordTextBlock('Heading 4', paragraph.text, current_heading_3)
            current_heading_3.child_blocks.append(current_heading_4)
            # print('\033[31mheading4\033[0m')
            # print('XML:')
            # element = paragraph._element
            # print(element.xml)

        if style == 'Normal':
            if current_heading_3: # Check if this is a 'Questions' or 'Answers' subchapter. In retrospect, I could have moved the 'if ignore_QnA' line to the top.
                para_text = current_heading_3.text_content
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

            item = MSWordTextBlock('Normal', paragraph.text, parent)
            if ilvl != None and numId != None: item.list_positioning = (ilvl,numId)
            if current_heading_4: 
                current_heading_4.child_blocks.append(item)
                # print('XML:')
                # element = paragraph._element
                # print(element.xml)
            elif current_heading_3: current_heading_3.child_blocks.append(item)

    return chapters

