# https://www.youtube.com/watch?v=WnGPv6HnBok&list=PLBmcuObd5An559HbDr_alBnwVsGq-7uTF

import pandas as pd
import spacy
from spacy import displacy

def has_golang(doc):
    # loop all documents
    for t in doc:
        if t.lower_ in ["go", "golang"]:
        # look for go where word is not a VERB
        # ADV is a pos_ property while advmod is a dep_ property
            if t.dep_ == 'pobj':
                return True
    return False


nlp = spacy.load("en_core_web_lg") # initialise model


#### HOW IT WORKS BASICS
print(type(nlp("My name is Theodore"))) # confirm it is a document
print([t for t in nlp("My name is Theodore")]) # confirm it is a collection

# zooming on the collection
doc = nlp("My name is Theodore")
print(type(doc[0]))
# visualise the sentence
'''displacy.serve(doc, style="dep", host="127.0.0.1") '''

for t in nlp("Where does Console.Writleine go in ASP.NET?"):
    print(t, t.pos_, t.dep_)

print(f"Definitions:", spacy.explain("ADV"),spacy.explain("AUX"),spacy.explain("ADP"),spacy.explain("PROPN"))
print("\n\n")


# text = "Can I append an Ajax requestXML object to my document tree all in one go?"
# displacy.serve(nlp(text), style="dep", host="127.0.0.1")

df = (pd.read_csv("Intro_to_NLP\Questions.csv", nrows=2_000_000,
                    encoding="ISO-8859-1", usecols=['Title','Id']))

titles = [_ for _ in df.loc[lambda d: d['Title'].str.lower().str.contains("go")]["Title"]]


# pipe is a spacy method which handles performance better
g = (doc_title for doc_title in nlp.pipe(titles) if has_golang(doc_title))
# regular text search will not work in case we are looking for go language
print([next(g) for i in range(5)]) # some magic


###### Part Two. More Intensive
# Function. if proper noun is mentioned
def has_go_token(doc):
    for t in doc:
        if t.lower_ in ["go", "golang"]:
           if t.dep_ == "pobj":
                return True
    return False

# Function. if there is mention of the word go
def has_go_mentioned(doc):
    for t in doc:
        if t.lower_ in ["go", "golang"]:
                return True
    return False

df_tags = pd.read_csv("Intro_to_NLP\Tags.csv")
go_ids = df_tags.loc[lambda d: d['Tag'] == 'go']['Id'] # put tags with the word go in list

all_go_Titles = df.loc[lambda d: d['Id'].isin(go_ids)]['Title'].tolist() # get the title taged with go
detectable = [d.text for d in nlp.pipe(all_go_Titles) if has_go_token(d)] # detect search word in title text

non_detectable = (df.loc[lambda d: ~d['Id'].isin(go_ids)] # get the NOT title taged with go
                        .loc[lambda d: d['Title'].str.lower().str.contains("go")]['Title'].tolist())

non_detectable = [d.text for d in nlp.pipe(non_detectable) if has_go_token(d)] # detect search word in title text

print(len(all_go_Titles),len(detectable),len(non_detectable))
print()


model_name = "en_core_web_lg"
model = spacy.load(model_name, disable=["ner"]) # disable a part of the pipeline to decrease processing time



method = "not-verb-but-pobj"
correct = sum(has_go_mentioned(doc) for doc in model.pipe(detectable))
wrong = sum(has_go_mentioned(doc) for doc in model.pipe(non_detectable))
precision = correct/(correct + wrong)
recall = correct/len(detectable)
accuracy = (correct + len(non_detectable) - wrong)/(len(detectable)+len(non_detectable))
print(f"precision:{precision}, recall:{recall}, accuracy:{accuracy}, model_name:{model_name}, method:{method}")
