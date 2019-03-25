import os
import glob
import re
import numpy as np
from tqdm import tqdm
from utils import draw_boxes
from frontend import YOLO
import json
import cv2
os.environ["CUDA_VISIBLE_DEVICES"]="-1"

# Keras
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image

# Flask utils
from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
weights_path = 'models/full_yolo_boat.h5'
config_path='config/config_NR_tiny_yolo.json'


with open(config_path) as config_buffer:
    config = json.load(config_buffer)

yolo = YOLO(backend = config['model']['backend'],
            input_size = config['model']['input_size'],
            labels = config['model']['labels'],
            max_box_per_image   = config['model']['max_box_per_image'],
            anchors             = config['model']['anchors'])

yolo.load_weights(weights_path)


from keras.layers import Flatten, Dense
x = yolo.model.output
x = Flatten()(x)
predictions = Dense(1024, activation=activType)(x)
model_final = Model(inputs =yolo.model.input, outputs = predictions,name='predictions')