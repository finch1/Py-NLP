# https://www.youtube.com/watch?v=i74DVqMsRWY&list=PL2VXyKi-KpYttggRATQVmgFcQst3z6OlX&index=7
# import nltk
# nltk.download()

import json
import glob
import re
from os import path

import pandas as pd
from pkg_resources import working_set
from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def load_data(file):
    with open (file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def write_data(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def append_data(filename):

    listObj = []
 
    # Check if file exists
    if path.isfile(filename) is False:
      raise Exception("File not found")
 
    # Read JSON file
    with open(filename) as fp:
        listObj = json.load(fp)
 
    print('Successfully loaded JSON file')        

    return listObj

def removeUnicodeChars(text):

    charDict = {"\u2013": "-",
                "\u2026": "...",
                "\u2019": "'",
                "\u0142": "l",
                "\u0105": "a",
                "\u0119": "e",
                "\u2014": "-",
                "\u2695": " ",
                "\u0101": "a",
                "\u0113": "e",
                "\u0144": "n",
                "\u2018": "'",
                "\u2022": " "}

    for key in charDict:    
        text = re.sub(key, charDict[key], text)
    

    return text

def clean_docs(_savedJobs):

    _cleaned_posts = []
    _position_posts = []

    for dict in _savedJobs:        
        text_with_bad_chars = dict['post']

        text = removeUnicodeChars(text_with_bad_chars)

        # remove punctuation
        unpunctuated = text.translate(str.maketrans("", "", string.punctuation))
        # get rid of all numbers
        numbers_removed = "".join([i for i  in unpunctuated if not i.isdigit()])


        stop_words = set(stopwords.words("english"))

        # split text into single words to remove stop words
        word_tokens =  word_tokenize(numbers_removed)

        filtered_sentences = [w for w in word_tokens if not w.lower() in stop_words] # returns array of text

        _cleaned_posts.append(" ".join(filtered_sentences))
        _position_posts.append(" ".join(dict['position']))

    return _cleaned_posts, _position_posts

# load specific key from file
savedJobs = append_data("SavedJobPosts.json")
# posts = ""
# for dict in savedJobs:
#     posts = posts + dict['post'] + "\n"

cleaned_posts, position_posts = clean_docs(savedJobs)

vectorizer = TfidfVectorizer(
                                lowercase=True,    # lowercase everything
                                max_features=100,   # 
                                max_df=0.8,         # if words dont occur in 80% of the document, they shall be ignored
                                min_df=15,           # if a word does not occur accross the whole corpus at least 5 times
                                ngram_range=(1,3),
                                stop_words="english")

vectors = vectorizer.fit_transform(cleaned_posts)

featured_names = vectorizer.get_feature_names_out()

dense = vectors.todense()
denselist = dense.tolist()

all_keywords = []

# extract the TFiDF results
for description in denselist:
    x = 0
    keywords = []
    for word in description:
        if word > 0:
            keywords.append(featured_names[x])
        x = x+1

    all_keywords.append(keywords)



# for i in range(len(all_keywords)):
#     print(all_keywords[i])

print('Successfull TFIDF')
print('K-Means to see overlap')

true_k = 20

model = KMeans(n_clusters=true_k, init="k-means++", max_iter=100, n_init=1)

model.fit(vectors)

order_centroids = model.cluster_centers_.argsort()[:,::-1]

terms = vectorizer.get_feature_names_out()

with open ("trc_results.txt", "w", encoding="utf-8") as f:
    for i in range(true_k):
        f.write(f"Cluster-{i}")
        f.write("\n")
        for ind in order_centroids[i, :10]:
            f.write(' %s' % terms[ind])
            f.write("\n")
        f.write("\n")
        f.write("\n")

# visualise highlighted tokens in original text
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

kmean_indices = model.fit_predict(vectors)

pca = PCA(n_components=2)

scatter_plot_points = pca.fit_transform(vectors.toarray())

colors = ["r", "b", "g", "c", "y", "m"]

x_axis = [o[0] for o in scatter_plot_points]
y_axis = [o[1] for o in scatter_plot_points]

fig, ax = plt.subplot(figsize=(50, 50))

ax.scatter(x_axis, y_axis, c=[colors[d] for d in kmean_indices])

for i, txt in enumerate(position_posts):
    ax.annotate(txt[0:5], (x_axis[i], y_axis[i]))

plt.savefig("trc.png")