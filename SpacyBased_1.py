import json
import spacy



with open ("NLP\data.txt", "r", encoding="utf-8") as f: # r for read
    text = f.read().split("\n\n")[3:4] # removes all line breakes. [] = work with first chunk of data
    # print(text)

segment = ""

# try grabbing the named entities
for segment in text:
    # print(segment)

    segment = segment.strip() # removes spaces from begining and end
    segment = segment.replace("\n"," ")
    # print()
    # print(segment)

    punc = '''!()-[]{};:'"\,<>?@£$%^&*_~'''
    punc = set(punc)
    segment = "".join(ch for ch in segment if ch not in punc)
    # print()
    print(segment)

nlp = spacy.load("en_core_web_lg")
doc = nlp(segment)
for ent in doc.ents:
    print(ent.text, ent.label_)