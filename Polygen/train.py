import os
import sys

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

'''
parser = argparse.ArgumentParser()

parser.add_argument('--log_dir', default='log', help='Log dir [default: log]')
parser.add_argument('--max_epoch', type=int, default=50, help='Epoch to run [default: 50]')
parser.add_argument('--batch_size', type=int, default=24, help='Batch Size during training [default: 24]')
parser.add_argument('--learning_rate', type=float, default=0.001, help='Initial learning rate [default: 0.001]')
parser.add_argument('--momentum', type=float, default=0.9, help='Initial learning rate [default: 0.9]')
parser.add_argument('--optimizer', default='adam', help='adam or momentum [default: adam]')
parser.add_argument('--decay_step', type=int, default=300000, help='Decay step for lr decay [default: 300000]')
parser.add_argument('--decay_rate', type=float, default=0.5, help='Decay rate for lr decay [default: 0.5]')
parser.add_argument('--input_list', type=str, default='data/train_hdf5_file_list_woArea5.txt', help='Input data list file')
parser.add_argument('--restore_model', type=str, default='log/', help='Pretrained model')
FLAGS = parser.parse_args()
'''

# Loading ShapeNet Dataset
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


ex_list = []
for mesh in train_data_paths:
    print(mesh)
    mesh_dict, flag = data_utils.load_process_mesh(
        os.path.join('meshes/ShapeNetCore.v2', '{}/models/model_normalized.obj'.format(mesh)))
    if flag:
        mesh_dict['class_label'] = data_utils.class_dict[mesh.split('/')[0]]
        ex_list.append(mesh_dict)

print(len(ex_list))
print('--------saving as numpy file---------------')
ex_np_list=np.array(ex_list)
np.save('meshes/ex_list.npy',ex_np_list)
print('----------------saved----------------------')
synthetic_dataset = tf.data.Dataset.from_generator(
    lambda: ex_list,
    output_types={
        'vertices': tf.int32, 'faces': tf.int32, 'class_label': tf.int32},
    output_shapes={
        'vertices': tf.TensorShape([None, 3]), 'faces': tf.TensorShape([None]),
        'class_label': tf.TensorShape(())}
)
ex = synthetic_dataset.make_one_shot_iterator().get_next()

# Inspect the first mesh
with tf.Session() as sess:
    ex_np = sess.run(ex)
print(ex_np)

# Plot first 4 meshes
mesh_list = []
with tf.Session() as sess:
    for i in range(4):
        ex_np = sess.run(ex)
        mesh_list.append(
            {'vertices': data_utils.dequantize_verts(ex_np['vertices']),
             'faces': data_utils.unflatten_faces(ex_np['faces'])})
data_utils.plot_meshes(mesh_list, ax_lims=0.4)

# Prepare the dataset for vertex model training
vertex_model_dataset = data_utils.make_vertex_model_dataset(
    synthetic_dataset, apply_random_shift=True)
vertex_model_dataset = vertex_model_dataset.repeat()
vertex_model_dataset = vertex_model_dataset.padded_batch(
    16, padded_shapes=vertex_model_dataset.output_shapes)
vertex_model_dataset = vertex_model_dataset.prefetch(16)
vertex_model_batch = vertex_model_dataset.make_one_shot_iterator().get_next()

# Create vertex model
vertex_model = modules.VertexModel(
    decoder_config=dict(
        hidden_size=512,
        fc_size=2048,
        num_heads=8,
        layer_norm=True,
        num_layers=24,
        dropout_rate=0.2,
        re_zero=True,
        memory_efficient=True
    ),
    quantization_bits=8,
    class_conditional=True,
    max_num_input_verts=5000,
    use_discrete_embeddings=True,
)
vertex_model_pred_dist = vertex_model(vertex_model_batch)
vertex_model_loss = -tf.reduce_sum(
    vertex_model_pred_dist.log_prob(vertex_model_batch['vertices_flat']) *
    vertex_model_batch['vertices_flat_mask'])
vertex_samples = vertex_model.sample(
    4, context=vertex_model_batch, max_sample_length=400, top_p=0.9,
    recenter_verts=True, only_return_complete=False)

# print(vertex_model_batch)
# print(vertex_model_pred_dist)
# print(vertex_samples)

face_model_dataset = data_utils.make_face_model_dataset(
    synthetic_dataset, apply_random_shift=True)
face_model_dataset = face_model_dataset.repeat()
face_model_dataset = face_model_dataset.padded_batch(
    16, padded_shapes=face_model_dataset.output_shapes)
face_model_dataset = face_model_dataset.prefetch(1)
face_model_batch = face_model_dataset.make_one_shot_iterator().get_next()

# Create face model
face_model = modules.FaceModel(
    encoder_config=dict(
        hidden_size=512,
        fc_size=2048,
        num_heads=8,
        layer_norm=True,
        num_layers=10,
        dropout_rate=0.2,
        re_zero=True,
        memory_efficient=True,
    ),
    decoder_config=dict(
        hidden_size=512,
        fc_size=2048,
        num_heads=8,
        layer_norm=True,
        num_layers=14,
        dropout_rate=0.2,
        re_zero=True,
        memory_efficient=True,
    ),
    class_conditional=False,
    decoder_cross_attention=True,
    use_discrete_vertex_embeddings=True,
    max_seq_length=8000,
)
face_model_pred_dist = face_model(face_model_batch)
face_model_loss = -tf.reduce_sum(
    face_model_pred_dist.log_prob(face_model_batch['faces']) *
    face_model_batch['faces_mask'])
face_samples = face_model.sample(
    context=vertex_samples, max_sample_length=2000, top_p=0.9,
    only_return_complete=False)
# print(face_model_batch)
# print(face_model_pred_dist)
# print(face_samples)


# Optimization settings
learning_rate = 3e-4
training_steps = 5000
check_step = 10

# Create an optimizer an minimize the summed log probability of the mesh
# sequences
optimizer = tf.train.AdamOptimizer(learning_rate)
vertex_model_optim_op = optimizer.minimize(vertex_model_loss)
face_model_optim_op = optimizer.minimize(face_model_loss)

# Training loop
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for n in range(training_steps):
        if n % check_step == 0:
            v_loss, f_loss = sess.run((vertex_model_loss, face_model_loss))
            print('Step {}'.format(n))
            print('Loss (vertices) {}'.format(v_loss))
            print('Loss (faces) {}'.format(f_loss))
            v_samples_np, f_samples_np, b_np = sess.run(
                (vertex_samples, face_samples, vertex_model_batch))
            mesh_list = []
            for n in range(4):
                mesh_list.append(
                    {
                        'vertices': v_samples_np['vertices'][n][:v_samples_np['num_vertices'][n]],
                        'faces': data_utils.unflatten_faces(
                            f_samples_np['faces'][n][:f_samples_np['num_face_indices'][n]])
                    }
                )
            data_utils.plot_meshes(mesh_list, ax_lims=0.5)
        sess.run((vertex_model_optim_op, face_model_optim_op))
