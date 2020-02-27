#!/usr/bin/env bash

python inference.py          \
    --dataset_folder '/raid/users/ebarnett/CV4A_psetae_data/test/' \
    --weight_directory ''\
    --geomfeat 0                \
    --d_k 13                    \
    --input_dim 13              \
    --batch_size 16             \
    --mlp1 '[13, 32, 64]'       \
    --mlp2 '[128, 128]'
