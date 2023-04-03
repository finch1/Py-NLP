## Spacy

word = 'Hello World'

# get character
word[0]

# count the number of occurances of a character in the string
word.count('l')

# index of substring
word.index(e)

# search for substring
word.find('World')

# search for last occurance
word.rfind('l')


# capitalize the first character
word.capitalize() ## capitalizes the first character

# title case ,eams to make a title, so each word has the first character capitalized
word.title()

# take a list of strings and joins them into one string
' '.join (['hello', 'world'])

# replacing a substring means changing all of its occurances with another string
'hello madam'.replace('hello', 'good morning') ## 'good morning madam'

# getting substring by index is called slicing using start index and end index
word = 'Hello Madam Flower'
word[6:11] 
> 'Madam'

# getting the first word, leave the first index blank 
word[:5]
> 'Hello'

# leaving second index blank returns till the end
word[12:]
> 'Flower'

## INSTALLING
pip install spacy # install
python -m spacy info # check version
pip install -U spacy # upgrade to latest version

## MODELS
# several pre trained models available:
en_core_web_sm
en_core_web_md
en_core_web_lg
# indicates language
# type indicates model capability; core means a general purpose model for the vocab
# ,syntax, entities and vectors
# genre is the type of text model recognizes: can be web, news, twitter...
# size: lg. md, sm

python -m spacy download en_core_web_md # insall model

## LOAD PACKAGES
import spacy # import spacy
nlp = spacy.laod('en_core_web_md') # returns a Language class instance, nlp. The Language class is the text processing pipeline
doc = nlp('I have a ginger cat') # Apply nlp on the sentence and got a Doc class instance, doc

# alternatley
pip install /Users/yourself/en_core_web_lg-2.0.0.tar.gz

import en_core_web_md
nlp = en_core_web_md.load() # this way, we can run the model in a local project

## DISPLAcY
'''
Merge Punctuation merges the punctuation into the previous token and
servers as more compact visualization (it works better for long documents)

Merge Phrases gives more compact dependency trees. This option merges
adjectives and nouns into one phrase; if you don't merge, then adjectives
and nouns will be displayed individually. EX:
They were beautiful and healty kids with strong appetites.

With both mergings:
They	were	beautiful and healthy kids	with strong appetites

Without any merging:
They 	were 	beautiful 	and 	healty 	kids 	with 	strong 	appetites.

Note: Law articles recomends merging
'''

'''
Entity visualizer highlights the named entities in the text. 
Entities = important nouns - names, places, dates, countries
'''
from spacy import displacy
displacy.serve(doc, style='dep', port='5000') # dep to the style parameter to see the dependency parsing result

'''
The chapter code can be found at the book's GitHub repository: https://github.
com/PacktPublishing/Mastering-spaCy/tree/main/Chapter02
'''

## THE PROCESS
'''
Calling nlp - first step is tokenization to produce a Doc object. 
	Tokenizer - Segments text into tokens
The Doc object is then processed further with a:
	Tagger - Assigns part-of-speach tags. Doc[i].tag
	Parser - Assigns dependency labels. Doc[i].head, Doc[i].dep, Doc.sents, Doc.noun_chunks
	Entity Recognizer - Detect and label named entities. Doc.ents, Doc[i].ent_iob, Doc[i].ent_type

This way of processing is called a language processing pipeline.
Each pipeline component returns the processed Doc and then passes
it to the next component:

							NLP
		____________________________________________
Text -> Tokenizer -> tagger -> parser -> ner -> ... -> Doc

The language class instanciated as nlp, applies all the preceding
pipeline steps to the input text. doc object contains tokens that are
tagged, lemmatized and marked as entities (where applicable)
''' 

## SPACY PROCESSING PIPELINE CLASSES
'''
Language - a text processing pipeline. Usually loaded once per process as nlp and pass the instance around the application
Tokenizer - segment text and create doc objects with the discovered segment boundaries
Lemmatizer - determine the base forms of words
Morphology - assign linguistic features like lemmas, noun case, verb tense etc, based on the word and its part of speech tag
Tagger - annotate part of speech tags on doc objects
DependencyParser - annotate sytactic dependencies on doc objects
Entityrecognizer - annotate named entities
TextCategorizer - assign categories or labels to doc objects
Matcher - match sequence of tokens, based on pattern rules, similar to regular expressions
PhraseMatcher - Match sequence of tokens, based on phrases
EntityRuler - add entity spans to the doc using token based rules or exact phrase matches
Sentencizer - implement custom sentence boundary detection logic that does not require the dependency parse
'''

## CONTAINER OBJECTS
'''
Doc - a container for accessing linguistic annotations (a sequence of Token objects)
Span - a slice from a doc object
Token - an individual token - i.e. a word, punctuation symbol, whitespace
Lexeme - an entry in the vocabulary. its a word type with no context as opposed to a word token. has no part of speech tag, dependency parse, etc.
'''

## OTHER CLASSES
'''
	Vocab
	StringStore
	Vectors
	GoldParse
	GoldCorpus
'''

## EXPLENATION
'''
Tokenization - splitting sentence into tokens - a unit of semantics,
i.e. as the smallest meaningful part of a piece of text.
Building blocks of a sentence: words, numbers, punctuation, currency symbols, etc...
Tokenization is based on language-specific rules. You can see examples the language specified data
here: https://github.com/explosion/spaCy/tree/master/spacy/lang.
'''

import spacy
nlp = spacy.load("en_core_web_lg") # load the En language model to create an instance of nlp Language class
doc = nlp("I own a ginger cat.") # returns a doc object
print([token.text for token in doc]) # = ['I', 'own', 'a', 'ginger', 'cat', '.']

