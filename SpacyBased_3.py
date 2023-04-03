# using trained data from previous example
# https://www.youtube.com/watch?v=YBRF7tq1V-Q&list=PL2VXyKi-KpYs1bSnT8bfMFyGS-wMcjesM&index=5
## CREATING CUSTOM TRAINING SET, WITH PARAGRAPH AND NAMES DETECTED POSITIONS

from typing import Pattern
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json
import csv
import random

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def test_model(model, text):
    doc = nlp(text)
    results = []
    entities = []
    for ent in doc.ents:
        entities.append((ent.start_char, ent.end_char, ent.label_)) # tuple spacy wants to see as training data
    
    if len(entities) > 0: # if entity has been found
        results = [text, {"entities": entities}] # what spacy wants to see fro training 
    return results

# TRAIN_DATA = [(text, {"entities":[(start, end, label)]})]
TRAIN_DATA = []

nlp = spacy.load("NLP\hp_ner")

with open ("NLP\data.txt", "r", encoding="utf-8") as f: # r for read
    text = f.read()

    # split the chapters
    chapters = text.split("CHAPTER")[1:]
    for chapter in chapters:
        chapter_num, chapter_title = chapter.split("\n\n")[0:2]
        chapter_num = chapter_num.strip()
        # print(chapter_num) 
        segments = chapter.split("\n\n")[2:]
        hits = []
        for segment in segments:
            # print(segment)

            segment = segment.strip() # removes spaces from begining and end
            segment = segment.replace("\n"," ")
            # print()
            # print(segment)

            punc = '''!()-[]{};:'"\,<>?@£$%^&*_~'''
            punc = set(punc)
            segment = "".join(ch for ch in segment if ch not in punc)
            # print(segment)
            results = test_model(nlp, segment)
            if results != None:
                TRAIN_DATA.append(results)

# this is the text and a list of mentioned names (the position and label)
save_data("NLP\hp_training_data.json", TRAIN_DATA)