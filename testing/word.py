from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

from data_extraction import read_doc
import generate as g

doc_tree = read_doc.get_document_tree('data/"ATPL Ground Training Series - Book 8 Human Performance and Limitations.docx"')
for main_node in doc_tree:
    print(main_node)

print('chapter 2 json string')
chapter2 = doc_tree[1].get_jsonstring()
print(chapter2)
print()
print()

print('chapter 2 dictionary')
ch2_dict = doc_tree[1].get_table_of_contents()
print(ch2_dict)
print()
print()

level3_names = []
for level3 in ch2_dict['Subitems']:
    name = level3['Name']
    name = name.strip()
    if name == 'Questions' or name == 'Answers': continue
    level3_names.append(name)

print(level3_names)
print()
print()

# for level3item in doc_tree[1]['Subitems']:

blood_circulation = doc_tree[1].child_blocks[2]
blood_circulation_json_string = blood_circulation.get_jsonstring()

response = g.generate_MCQ_json(blood_circulation_json_string)
print(response)