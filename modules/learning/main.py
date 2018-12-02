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
from sklearn.cluster import DBSCAN


def gen_dataset():
    disciplines, features_name, dataset = get_term_frequency_from_keywords(apply_stem= True, n_keywords=50)
    # np.savetxt("dataset.csv", dataset, delimiter=";", fmt='%s')
    return disciplines, features_name, np.asarray(dataset)

def apply_clustering(disciplines, features_name, dataset, n_clusters=20, classifier='kmeans', eps=0.5, min_samples=5):
    date_string = datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')
    os.mkdir(date_string)

    if classifier == 'kmeans':
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(dataset)
        results = kmeans.predict(dataset)
    if classifier == 'dbscan':
        dbscan = DBSCAN(eps=eps, min_samples=min_samples).fit(dataset)
        results = dbscan.labels_

    for i in range(0, len(results)):
        with open('{}/cluster_{}'.format(date_string, results[i]), 'a+') as file:
            file.write(disciplines[i].encode('utf-8', 'ignore'))
            file.write('\n')
            file.close()

import time
start_time = time.time()
disciplines, features_name, dataset = gen_dataset()
apply_clustering(disciplines, features_name, dataset, n_clusters=40, classifier='kmeans')

# for i in [50, 100, 150, 200]:
# apply_clustering(disciplines, features_name, dataset, n_clusters=i, classifier='kmeans')
    # print('applying clustering')

# for i in [4.0, 4.5, 5.0, 5.5, 6, 6.5]:
#     print('applying clustering')
#     apply_clustering(disciplines, features_name, dataset, n_clusters=100, classifier='dbscan', min_samples=2, eps=i)


print("--- time elapsed: %s seconds ---" % (time.time() - start_time))
# import pdb; pdb.set_trace()
