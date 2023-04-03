'''
What do they want that they do not already have?
'''

# import libraries
from fileinput import filename
import numpy as np
import json
import regex as re

import datetime
e = datetime.datetime.now()

import os
from os import path

# Spacy
import spacy
nlp = spacy.load("en_core_web_sm")

# NLTK
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer(language='english')

# VIS
# !pip install pyLDAvis
import pyLDAvis
import pyLDAvis.gensim_models

print ("The time is now: = %s:%s:%s" % (e.hour, e.minute, e.second))
os.chdir(r'C:\\Users\\bminn\\Documents\\PROJECT INVESTIGATION\\NLP\\ExtractJobPost\\')
print(os.getcwd())

# load json data
def load_json(filename):

    listObj = []

    # Check if file exists
    if path.isfile(filename) is False:
        raise Exception("File not found")
 
    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
 
    print('Successfully loaded JSON file\n')        

    return listObj

# save json data
def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print('Successfully saved JSON file\n')   

# load specific key from file
savedJobs = load_json("SavedJobPosts - Copy - Copy.json")

# deep clean text
def deep_clean(uncleaned_text):
        
    # remove unicode characters completly. 
    string_encode = uncleaned_text.encode("ascii", "ignore")
    uncleaned_text = string_encode.decode()

    # lower case everything
    stage_1 = uncleaned_text#.lower()
    
    # get rid of all numbers
    #stage_2 = "".join([i for i  in stage_1 if not i.isdigit()])

    # remove punctuation
    char_dict = {   "/": " ", 
                    "(": " ", 
                    ")": " ",
                    ",": " ", 
                    "-": " ", 
                    "+": " ",
                    ";": " ",
                    ":": " ",
                    "!": ".",
                    "<": " ",
                    ">": " ",
                    "&": " "}

    stage_3 = stage_1.translate(str.maketrans(char_dict))
    
    pattern = [                
                "\\n", # new line
                "\.\.+\.", # multiple dots
                "\\\"", # found in foreign language posts
                "(?!\s\n)\s+\s" # match two or more space but not space at the end of a string followed by a new line
                ]
    
    for p in pattern:
        stage_3 = re.sub(p, ' ', stage_3)

    #string_list2 = [s.strip() for s in string_list1 if s != '']

    return stage_3

# clean the job posts main data
def clean_docs(_savedJobs):

    #_cleaned_posts = []
    #_position_posts = []

    for dict in _savedJobs:
        if (not 'cleaned_post' in dict): # if does not exists / if text is not yet cleaned
            dict['cleaned_post'] = deep_clean(dict['post'])            
            # _cleaned_posts.append(post)
        
    return _savedJobs

# lemmatize each post
# Lemmatization converts words in the second or third forms to their first form variants.
def lemma_docs(_savedJobs):
    for dict in _savedJobs:
        if not 'spaCy_lemma_w_stop' in dict: # if does not exists / if text is not yet lemmatized
            doc = nlp(dict['cleaned_post'])
            lemma = [token.lemma_ for token in doc]
            dict['spaCy_lemma_w_stop'] = " ".join(lemma)            
            dict['spaCy_lemma_w_stop'] = str(dict['spaCy_lemma_w_stop']).replace(" . ", ". ").replace(" ? ", "? ") # error correction after lemma

            dict['spaCy_lemma_wo_stop'] = " ".join([token.lemma_ for token in doc if not token.is_stop])
            dict['spaCy_lemma_wo_stop'] = str(dict['spaCy_lemma_wo_stop']).replace(" . ", ". ").replace(" ? ", "? ")  # error correction after lemma

    return _savedJobs

# STEM
def stemming(_savedJobs):
     
    for dict in _savedJobs:
        if not 'NLTK_SB_stem' in dict: # if does not exists / if text is not yet lemmatized
            tokenized = word_tokenize(str(dict['spaCy_lemma_wo_stop']))
            snowball_stem = [stemmer.stem(token) for token in tokenized]
            
            dict['NLTK_SB_stem'] = " ".join(snowball_stem).replace(" . ", ". ").replace(" ? ", "? ") # error correction after stemming
            
    return _savedJobs


# split into senteces
def to_senteces(_savedJobs):

    # what immediatly precceds the capital letter is a full stop and space (?<=\.\s)[A-Z]
    # look for full stop \.\s
    # disect senteces 
    pattern = r'[?<=[\.\s]]^|[A-Z].*?[?=\.]' # round brackets will screw you over. use square brackets instead.
    for dict in _savedJobs:
        if not 'sentences' in dict: # if does not exists
            _post = dict['cleaned_post']
            dict['sentences'] = re.findall(pattern, _post)

    return _savedJobs

# extract experience, qualifications and requirements from senteces
def exp_req(_savedJobs):

    _patterns = [r'\bqualification\b', r'\bqualify\b', r'\bequivalent\b', r'\brequir\b', r'\bexperience\b', r'\bcertificat\b', r'\d.*\d\syear|\d\syear']
    
    for dict in _savedJobs:
        if not 'exp_req' in dict: # if does not exists
            asking_for = []
            for sentence in dict['sentences']:

                for _pattern in _patterns:
                    match = re.search(_pattern,sentence)
                    if match:
                        asking_for.append(sentence)                    

            # This is the fastest and smallest method to achieve a particular task. It first removes the duplicates and returns a dictionary which has to be converted to list. 
            if asking_for: # if not empty
                dict['exp_req'] =  [*set(asking_for)]

    return _savedJobs

## To ADD
## Hash clean text to find duplicates
## Sentence segmentation
## Vectors
## Rule-based Matching
## in stemmer, try adding dictionary of original token and its stem to group and compare with original. Am not sure what the stemmer is used for, just word embeddings for now
## on match collect sentence. We can then analyze their POS to come up with more matches
## important words scoring
## bundle skills and tools required for job title. 
## https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa
## how to write an experience point in a CV 
# Drove customer loyalty by delivering high quality food service and wine pairing suggestions to an average of 100 customers an evening during peek business hours.
# Spearheaded a project to increase foot traffic to our retail store which was successful in driving sales up by 15%.
# Authored the bi-monthly company newsletter that was directly responsible for enlisting at least 5 new subscribers each month.
# Built and motivated an international team to adjust our product for international markets that increased our sales by 60%.
# Overhauled our operating systems which increased production output by 35%.
# Improved the arrangements in the kitchen which allowed staff to move more freely and so improved efficiency.
# Consolidated the Software Development Roadmap to ensure all critical projects were completed on time.
# Suggested a new layout in the beverage supply closet which improved the servers' efficiency by 15%.
# Audited companies in various industry sectors for financial discrepancies and maintained a 95% accuracy rate.

## came across "developing and maintaining". how can i capture combinations?
## extract words from the pdf books i read. keep occurance of 1. add to my words list
## https://dictionaryapi.dev/
## https://developer.oxforddictionaries.com/
## https://dictionaryapi.com/
## mirror the language of the job description. use the sentences where the skills and requirements are listed
## word2vec to analyse categories
## remove stop words to analyse TFIDF
## verb and adverbs as requirements and skills
## IT Tools - capitals maybe?
## Clip = multi modal model by openAI

## compare tools required with Data Engineering road map to configure learning path


## MAIN CODE
CleanedsavedJobs = clean_docs(savedJobs)

## LEMMATIZE
lemmatized_posts = lemma_docs(CleanedsavedJobs)

## STEMMING
stemmedText = stemming(lemmatized_posts)

## SPLIT INTO SENTENCES FOR SYNTACTIC COMPARISON
with_sentences = to_senteces(stemmedText)

## FIND REQUREMENTS
with_their_needs = exp_req(with_sentences)

write_data("SavedJobPosts - Copy - Copy.json", with_their_needs)
