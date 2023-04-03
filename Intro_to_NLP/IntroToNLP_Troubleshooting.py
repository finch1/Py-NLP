# https://www.youtube.com/watch?v=KL4-Mpgbahw&list=PLBmcuObd5An559HbDr_alBnwVsGq-7uTF&index=2
# the propblem is in case of searching "objective-c", spacy will tokenize  the title to:
# [i, am, an, iOS, dev, i, like, to, program, in, objective, -, c]

from re import match
from typing import Pattern
import pandas as pd
import spacy
from spacy import displacy
from spacy import matcher
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_lg") # initialise model

df = (pd.read_csv("Intro_to_NLP\Questions.csv", nrows=2_000_000,
                    encoding="ISO-8859-1", usecols=['Title','Id']))

titles = (_ for _ in df['Title'] if "objective" in _.lower())


objc_pattern1 = [{'LOWER': 'objective'},{'IS_PUNCT': True},{'LOWER':'c'}]
golang_pattern1 = [{'LOWER': {'IN': ["go", "golang"]},'POS': {"NOT_IN" : ["VERB"]}}]
golang_pattern2 = [{'LOWER': {'IN': ["go", "golang"]},'POS': {"NOT_IN" : ["VERB"]}}]

python_pattern1 = [{'LOWER': 'python'}]
ruby_pattern1 = [{'LOWER': 'ruby'}]
js_pattern1 = [{'LOWER': {'IN': ["js", "javascript"]}}]


mattcher = Matcher(nlp.vocab)
# add pattern. has three parts: Name, callback, pattern
mattcher.add("OBJC_LANG", [objc_pattern1])
mattcher.add("GOLANG_LANG", [golang_pattern1, golang_pattern2])
mattcher.add("PY_LANG", [python_pattern1])
mattcher.add("RB_LANG", [ruby_pattern1])
mattcher.add("JS_LANG", [js_pattern1])

for i in range(200):
    doc = nlp(next(titles))
    if len(mattcher(doc)) == 0:
        print(doc)
        print([t for t in doc])

