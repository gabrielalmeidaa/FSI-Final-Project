import nltk
import pymongo
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer, TfidfTransformer, CountVectorizer
from nltk.stem import RSLPStemmer
from sklearn.cluster import KMeans
import numpy as np
import sys
sys.dont_write_bytecode = True
import os
clear = lambda: os.system('clear')
import csv

''' Get Mongodb collection '''
def get_mongo_collection(collection_name):
    client = MongoClient('localhost', 27017)
    db = client['mw']
    collection = db[collection_name]
    return collection

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)

def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    """get the feature names and tf-idf score of top n items"""
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []
    # word index and corresponding tf-idf score
    for idx, score in sorted_items:
        #keep track of feature name and its corresponding score
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score
    results = zip(feature_vals,score_vals)
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results

def get_term_frequency_from_keywords(binary_weight=True, n_keywords=50, count_vectorizer_stop_words=None, count_vectorizer_min_df=0.0, count_vectorizer_max_df=0.9):
    descriptions = []
    disciplines = []
    return_data = []
    collection = get_mongo_collection('discipline')
    for item in collection.find():
        if item.get('programa'):
            name = item.get('nome')
            description = item.get('programa')
            descriptions.append(description)
            disciplines.append(name)

    ''' Creating word vectorizer '''
    cv = CountVectorizer(min_df= count_vectorizer_min_df, max_df=count_vectorizer_max_df, stop_words=count_vectorizer_stop_words)
    word_count_vector = cv.fit_transform(descriptions)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
    tfidf_transformer.fit(word_count_vector)

    feature_names=cv.get_feature_names()

    for i in range(0, len(descriptions)):
        # print('looping through descriptions')
        clear()
        print('missing {}'.format(len(descriptions) - i))
        tf_idf_vector=tfidf_transformer.transform(cv.transform([descriptions[i]]))
        sorted_items=sort_coo(tf_idf_vector.tocoo())
        keywords=extract_topn_from_vector(feature_names, sorted_items, n_keywords)
        keyword_indexes = [ feature_names.index(k) for k in keywords]
        if binary_weight:
            features_array = [1 if i in keyword_indexes else 0 for i in range(0, len(feature_names))]
        else:
            features_array = [keywords[feature_names[i]] if i in keyword_indexes else 0 for i in range(0, len(feature_names))]
        return_data.append(features_array)


    return disciplines, feature_names, return_data

            # return_data.append([[disciplines[i]] + k])
        # for k in keywords:
        #
        # # now print the results
        # # print("\n=====Doc=====")
        # # print(descriptions[i])
        # # print("\n===Keywords===")
        # for k in keywords:
        #     return_vals['keywords'].append(feature_names.index(k))
        #     # print(k,keywords[k])
        # # import pdb; pdb.set_trace()
        # full_return.append(return_vals)
        # return full_return

    # import pdb; pdb.set_trace()

        # import pdb; pdb.set_trace()
# disciplines, features_name, dataset = get_term_frequency_from_keywords()
# import pdb; pdb.set_trace()
# collection = get_mongo_collection('discipline')
# disciplines, features_name, dataset = get_term_frequency_from_keywords()
# import pdb; pdb.set_trace()
#
