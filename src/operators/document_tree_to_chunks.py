from src.models.chunk import Chunk
from src.models.msword_text_block import MSWordTextBlock


def document_tree_to_chunks(tree: list[MSWordTextBlock], book_name: str) -> list[Chunk]:
    """Given a document tree (like the output of the `get_dcocument_tree` function), 
    returns chunks that can be used in a RAG system.

    Each subchapter of a chapter is a chunk. This works well for the ATPL textbooks, as
    there're few references in between subchapters across the book. Therefore we can work with
    no chunk overlap.

    Args:
        tree (list[MSWordTextBlock]): _description_

    Returns:
        list[Document]: list of chunks (as langchain documents)
    """
    chunks: list[Chunk] = []
    was_previous_block_list = False

    for chapter in tree:
        for subchapter in chapter.child_blocks:

            markdown = f"# {chapter.text_content}\n"
            markdown += f"## {subchapter.text_content}\n"

            leaves = subchapter.get_leaves()
            current_heading4 = ''
            for leaf in leaves:
                if leaf.parent_block.level == 'Heading 4' and leaf.parent_block.text_content != current_heading4: # we have a new heading4
                    current_heading4 = leaf.parent_block.text_content
                    markdown += f'\n\n### {leaf.parent_block.text_content}: \n'
                elif leaf.parent_block.level == 'Heading 4' and leaf.parent_block.text_content == current_heading4: # we are still inside a previous heading4
                    pass
                else: # we have exited the domain of the heading4
                    current_heading4 = ''
                    markdown += '\n\n'
                
                if isinstance(leaf.list_positioning, tuple): # if it's a ms word list, add markdown bullet points
                    markdown += "- " + leaf.text_content + '\n'
                    was_previous_block_list = True
                else:
                    if was_previous_block_list:
                        was_previous_block_list = False
                        markdown += "\n" + leaf.text_content + '\n'
                    else:
                        markdown += leaf.text_content + '\n'

            chunks.append(Chunk(
                chapter=chapter.text_content,
                subchapter=subchapter.text_content,
                markdown=markdown,
                bookname=book_name,
            ))

    return chunks