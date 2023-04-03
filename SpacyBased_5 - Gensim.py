# https://www.youtube.com/watch?v=6HM75qOsgkU&list=PL2VXyKi-KpYs1bSnT8bfMFyGS-wMcjesM&index=10
# https://www.kaggle.com/pierremegret/gensim-word2vec-tutorial


import json
from gensim.models.word2vec import Word2Vec
from gensim.models.keyedvectors import KeyedVectors
import multiprocessing

from numpy import positive

def training(model_name):
    with open("NLP\hp_training_data.json", "r", encoding="utf-8") as f:
        texts = json.load(f)
    sentences = texts
    cores = multiprocessing.cpu_count()
    w2v_model = Word2Vec(
                            min_count=5, 
                            window=2,
                            vector_size=500, 
                            sample=6e-5, 
                            alpha=0.03, 
                            min_alpha=0.0007, 
                            negative=20, 
                            workers=cores-1)
    w2v_model.build_vocab(texts)
    w2v_model.train(texts, total_examples=w2v_model.corpus_count, epochs=30)
    w2v_model.save(f"word_vectors/{model_name}.model")
    w2v_model.wv.save_word2vec_format(f"word_vectors/word2vec_{model_name}.txt")

def gen_similarity(word):
    model = KeyedVectors.load_word2vec_format("word_vectors/word2vec_hp_ner_model_03.txt", binary=False)
    results = model.most_similar(positive=[word])
    print(results)

training("hp_ner_model_03")
gen_similarity("Harry")