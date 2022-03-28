import tensorflow as tf
import rasterio as rio
import netCDF4 as nc
import numpy as np
import os

import resnet

import argparse
import json
import os

from make_config import *
from dataloader import *


parser = argparse.ArgumentParser()
parser.add_argument("rank")
args = parser.parse_args()

direc = "/sciclone/home20/hmbaier/tflow/ips/"

os.environ["TF_CONFIG"] = make_config(int(args.rank) - 1, direc, 45962)

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()


IMAGERY_DIR = "/sciclone/scr-mlt/hmbaier/cropped/"
files = os.listdir(IMAGERY_DIR)
files = [IMAGERY_DIR + i for i in files if "484" in i][0:100]

cc = tf.keras.layers.CenterCrop(1000, 1000)


def get_train():

    for file in files:
        print("File: ", file)
        img = ( cc(np.array(nc.Dataset(file, "r")["ims"][0:1])[0] ), np.array(nc.Dataset(file, "r")["migrants"][0:1]) )
        yield img

def get_val():

    for file in files:
        img = np.array([[1], [1], [1], [1], [1], [1], [1], [1], [1], [1]])
        yield img


dataset = tf.data.Dataset.from_generator(generator = get_train,
                                         output_types=(tf.float32, tf.float32)).batch(10)


with strategy.scope():

    dataset = strategy.experimental_distribute_dataset(dataset)

    multi_worker_model = resnet.resnet56(img_input = tf.keras.layers.Input((None, None, 3)), classes = 1)

    multi_worker_model.compile(
        optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001),
        loss = tf.keras.losses.MeanAbsoluteError(),
        metrics=[tf.keras.losses.MeanAbsoluteError()]
    )

# Train model on dataset
multi_worker_model.fit(dataset,
                    steps_per_epoch = int(100 // 10))#,
                    # validation_data=validation_generator,
                    # use_multiprocessing=True,
                    # workers=6)