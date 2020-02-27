#!/usr/bin/env bash

python train.py          \
    --dataset_folder '/raid/users/ebarnett/CV4A_psetae_data/train/' \
    --geomfeat 0 \
    --d_k 13 \
    --kfold 5 \
    --lr 0.001 --npixel 3 --input_dim 13 --batch_size 64  \
    --mlp1 '[13, 32, 64]' \
    --mlp2 '[128, 128]'   \
    --mlp3 '[512, 128, 128]'   \
    --mlp4 '[128, 64, 32, 20]' \
    --num_classes 7 \
    --epochs 200
