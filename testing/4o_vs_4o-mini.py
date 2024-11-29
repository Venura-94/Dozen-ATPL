import pickle

from src.MCQ import MCQ

with open('extracted_data/mcqs first 5 - 4o.pkl','rb') as file:
    mcqs_4o: list[MCQ] = pickle.load(file)

with open('extracted_data/mcqs first 10 - 4o-mini.pkl','rb') as file:
    mcqs_4oMini: list[MCQ] = pickle.load(file)
mcqs_4oMini = mcqs_4oMini[:5]

print('4o'); print()
for i,mcq in enumerate(mcqs_4o):
    print(f'MCQ {i+1}')
    print(mcq)
    print()

print();print();print('4o mini'); print()
for i,mcq in enumerate(mcqs_4oMini):
    print(f'MCQ {i+1}')
    print(mcq)
    print()

