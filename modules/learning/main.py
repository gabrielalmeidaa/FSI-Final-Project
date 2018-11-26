from stemming import get_term_frequency_from_keywords
import csv
import numpy as np


disciplines, features_name, dataset = get_term_frequency_from_keywords()
np.savetxt("dataset.csv", dataset, delimiter=";", fmt='%s')
import pdb; pdb.set_trace()
