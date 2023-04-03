# using trained data from previous example
# https://www.youtube.com/watch?v=7Z1imsp6g10&list=PL2VXyKi-KpYs1bSnT8bfMFyGS-wMcjesM&index=6

from typing import Pattern
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
from spacy.training import Example
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

def train_spacy(data, iterations): # number of times the model will go over the training data to learn.
    TRAIN_DATA = data
    nlp = spacy.blank("en") # blank model
    # if the model does not have ner pipeline
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner") # this holds tokenization, lemmitixation etc...

    for _, annotations in TRAIN_DATA: # grab all entities
        for ent in annotations.get("entities"): # loop each entity
            ner.add_label(ent[2]) # some models might have more than one label, so we grab them all

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.initialize()

        for itn in range(iterations):
            print("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA) # randomise so mode does not memorize ( overfit )
            losses = {}

            for raw_text, entity_offsets in TRAIN_DATA:
                doc = nlp.make_doc(raw_text)
                example = Example.from_dict(doc, entity_offsets)
                nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)
                print(losses)

    return nlp

# LOAD TRAINING DATA FROM PREVIOUS EXAMPLE
TRAIN_DATA = load_data("NLP\hp_training_data.json")
nlp = train_spacy(TRAIN_DATA, 30)
nlp.to_disk("NLP\hp_ner_model")

## to be continued

