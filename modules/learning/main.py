# from Tkinter import *
from data_setting import get_term_frequency_from_keywords
import csv
import numpy as np
from io import StringIO
import matplotlib
matplotlib.use('agg')
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from matplotlib import interactive
interactive(True)
from datetime import datetime
import os


def gen_dataset():
    disciplines, features_name, dataset = get_term_frequency_from_keywords(apply_stem= True)
    # np.savetxt("dataset.csv", dataset, delimiter=";", fmt='%s')
    return disciplines, features_name, np.asarray(dataset)


def read_dataset_from_csv():
    print('reading from csv...')
    dataset = np.genfromtxt('dataset.csv', delimiter=';')
    print('csv read')
    disciplines, features_name = get_term_frequency_from_keywords(no_dataset= True)
    return disciplines, features_name, dataset

# def k_means(n=20):
#     y_kmeans = kmeans.predict(X)
def apply_clustering(disciplines, features_name, dataset, n_clusters=20, classifier='kmeans'):
    date_string = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    os.mkdir(date_string)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(dataset)
    y_kmeans = kmeans.predict(dataset)
    for i in range(0, len(y_kmeans)):
        with open('{}/cluster_{}'.format(date_string,y_kmeans[i]), 'a+') as file:
            file.write(disciplines[i].encode('utf-8', 'ignore'))
            file.write('\n')
            file.close()
    # import pdb; pdb.set_trace()

import time
start_time = time.time()
disciplines, features_name, dataset = gen_dataset()
apply_clustering(disciplines, features_name, dataset, n_clusters=100 )

print("--- time elapsed: %s seconds ---" % (time.time() - start_time))
import pdb; pdb.set_trace()
