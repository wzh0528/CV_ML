import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(os.path.join(BASE_DIR, 'meshes/'))
print(BASE_DIR, DATA_DIR)

import numpy as np
import tensorflow.compat.v1 as tf

tf.logging.set_verbosity(tf.logging.ERROR)  # Hide TF deprecation messages

import argparse

import data_utils

parser = argparse.ArgumentParser()
parser.add_argument('--start_index', type=int, default=0, help='Start index  to filter [default: 0]')
parser.add_argument('--end_index', type=int, default=50000, help='End index to filter [default: 50000]')
FLAGS = parser.parse_args()

start_index = FLAGS.start_index
end_index = FLAGS.end_index


for key in data_utils.class_dict:
    data_path = ('meshes/meshes_np/' + key)
    if not os.path.exists(data_path):
        os.mkdir(data_path)

data_paths = [line.rstrip() for line in open(os.path.join(BASE_DIR, 'all.csv'))]
data_paths.pop(0)

train_data_paths = []
test_data_paths = []
val_data_paths = []
print('filtering from '+start_index+' to '+end_index)
for p in data_paths[start_index, end_index]:
    elements = p.split(',')
    if elements[4] == 'train':
        train_data_paths.append('0' + elements[1] + '/' + elements[3])
    elif elements[4] == 'test':
        test_data_paths.append('0' + elements[1] + '/' + elements[3])
    else:
        val_data_paths.append('0' + elements[1] + '/' + elements[3])
print('start filtering traindatas')
with open("train_data.txt", "a+") as f:
    for mesh in train_data_paths:
        if os.path.isfile(os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh))):
            print(mesh)
            mesh_dict, flag = data_utils.load_process_mesh(
                os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh)))
            if flag:
                f.write(mesh + '\n')
                np.save('meshes/meshes_np/' + mesh + '.npy', mesh_dict)

print('start filtering testdatas')
with open("test_data.txt", "a+") as f:
    for mesh in test_data_paths:
        if os.path.isfile(os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh))):
            print(mesh)
            mesh_dict, flag = data_utils.load_process_mesh(
                os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh)))
            if flag:
                f.write(mesh + '\n')
                np.save('meshes/meshes_np/' + mesh + '.npy', mesh_dict)

print('start filtering valdatas')
with open("val_data.txt", "a+") as f:
    for mesh in val_data_paths:
        if os.path.isfile(os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh))):
            print(mesh)
            mesh_dict, flag = data_utils.load_process_mesh(
                os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh)))
            if flag:
                f.write(mesh + '\n')
                np.save('meshes/meshes_np/' + mesh + '.npy', mesh_dict)
print('done')
