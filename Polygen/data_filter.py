BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(os.path.join(BASE_DIR, 'meshes/'))
print(BASE_DIR, DATA_DIR)

import numpy as np
import tensorflow.compat.v1 as tf

tf.logging.set_verbosity(tf.logging.ERROR)  # Hide TF deprecation messages
import matplotlib.pyplot as plt
import argparse

import modules
import data_utils

data_paths = [line.rstrip() for line in open(os.path.join(BASE_DIR, 'all.csv'))]
data_paths.pop(0)
print(len(data_paths))
train_data_paths = []
test_data_paths = []
val_data_paths = []
for p in data_paths:
    elements = p.split(',')
    if elements[4] == 'train':
        train_data_paths.append(elements[1] + '/' + elements[3])
    elif elements[4] == 'test':
        test_data_paths.append(elements[1] + '/' + elements[3])
    else:
        val_data_paths.append(elements[1] + '/' + elements[3])