from typing import Pattern
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json
import csv


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def generate_better_characters(file):
    data = load_data(file)
    new_characters = []

    for item in data:
        new_characters.append(item)

    for item in data:
        item = item.replace("The ","").replace("the ","").replace("and ","").replace("And ","")
        names = item.split(" ") # split names by space into array
        for name in names:
            name = name.strip()
            # print(name)
            new_characters.append(name)
    # this is to fix () in Al (Mad-Eye) Moody
        if "(" in item: # split by ( into array
            names = item.split("(")
            for name in names:
                name = name.replace(")", "").strip()
                new_characters.append(name)

        if "," in item:
            names = item.split(",")
            for name in names:
                name = name.replace("and", "").strip()
                new_characters.append(name)
                if " " in name:
                    new_names = name.split()
                    for x in new_names:
                        new_characters.append(x)
                        # print(x)

    # cater for special cases. Appending prefix on every name just in case its mentioned this eay 
    final_characters = []
    titles = ["Dr.", "Professor", "Mr.", "Mrs.", "Ms.", "Miss", "Aunt", "Uncle", "Mr. and Mrs."]
    print(len(new_characters))    
    for character in new_characters:
        final_characters.append(character)
        for title in titles:
            titled_char = f"{title} {character}"
            final_characters.append(titled_char)

    # 1D to 2D
    # final_characters = map(lambda split_str: split_str.split(','), final_characters)

    # with open("NLP\\nameslist.csv", 'w') as f:
    #     write = csv.writer(f)
    #     write.writerows(final_characters_new)

    # deleting dublicates. convert to set, which cannot have dublicates, then to list again
    final_characters = list(set(final_characters))
    # print(len(final_characters))

    # remove any blank data
    final_characters = [ x for x in final_characters if x != "" ]
    # print(len(final_characters))
    return (final_characters)           

def create_training_data(file, type):
    data = generate_better_characters(file)
    # create a dictionary of patterns
    patterns = []
    for item in data:
        pattern = {"label": type, "pattern":item}
        patterns.append(pattern)

    return patterns

def generate_rules(patterns):
    nlp = English()
    ruler = EntityRuler(nlp)
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    nlp.to_disk("NLP\hp_ner")

def test_model(model, text):
    doc = nlp(text)
    results = []
    for ent in doc.ents:
        results.append(ent.text)
    
    return results

def save_data(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# only need to generate one time. then load from disk
# labeled_data = create_training_data("NLP\HPNames.json", "PERSON")
# generate_rules(labeled_data)

nlp = spacy.load("NLP\hp_ner")
ie_data = {} # hits dictionary

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
            for result in results:
                hits.append(result)
            
        ie_data[chapter_num] = hits

# print(ie_data)        
save_data("NLP\hitsResults.json", ie_data)