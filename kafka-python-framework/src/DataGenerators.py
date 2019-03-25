import base64
from datetime import datetime
import time
from base64 import b64encode
import os
from uuid import uuid4
from random import randint
from swat import *

import sys
#sys.path.append(dlpy_path)
from dlpy.model import *
from dlpy.layers import *
from dlpy.applications import *
from dlpy.utils import *
from dlpy.images import ImageTable
from dlpy.splitting import two_way_split
from dlpy.blocks import *
import cv2
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import display
from dlpy.utils import input_table_check, random_name


from dataUtils.avroUtils import User, ImageRecord, SapImageRecord


def getUserRecords():
    userRecordList = list()

    names = ["olivier","tuula","cedric","melanie","isabelle","mark"]
    numbers = [15,9,8,7,6,5]
    colors = ["blue", "green", "pink", "yellow","black","white"]

    for i in range(6):
        userRecordList.append(User(names[i],numbers[i],colors[i]))

    return userRecordList




def getImageRecords():
    imageRecordList = list()
    with open(r"C:\Users\othierie\AlaskanMalamute.jpg", "rb") as imageFile:
        f = imageFile.read()
        b = str(b64encode(f))

    print(b)
    timeStampList = [datetime.now().microsecond,datetime.now().microsecond,datetime.now().microsecond,datetime.now().microsecond]
    numberOfBoatList = [0,1,2,3]
    ratioOfBoatList = [0,0.5,0.8,0.3]

    for i in range(4):
        imageRecordList.append(ImageRecord(timeStampList[i],numberOfBoatList[i],ratioOfBoatList[i],b))

    return imageRecordList


def getSapImagesFromDir():
    imageRecordList = list()
    files = findFilesInFolder(r"C:\imgTest",list(),"jpg",False)[0]
    imgs = [open(f , 'rb').read() for f in files]
    for img in imgs:
        imageRecordList.append(SapImageRecord(str(uuid4()),round(datetime.now().microsecond),1,0.5))

    return imageRecordList
def findFilesInFolder(path, pathList, extension, subFolders = True):
    """  Recursive function to find all files of an extension type in a folder (and optionally in all subfolders too)

    path:        Base directory to find files
    pathList:    A list that stores all paths
    extension:   File extension to find
    subFolders:  Bool.  If True, find files in all subfolders under path. If False, only searches files in the specified folder
    """
    print("find in Folder")
    try:   # Trapping a OSError:  File permissions problem I believe
        for entry in os.scandir(path):
            if entry.is_file() and entry.path.endswith(extension):
                pathList.append(entry.path)
            elif entry.is_dir() and subFolders:   # if its a directory, then repeat process as a nested function
                pathList = findFilesInFolder(entry.path, pathList, extension, subFolders)
    except OSError:
        print('Cannot access ' + path +'. Probably a permissions error')

    return [pathList,len(pathList)]

def getImagesFromDir():
    imageRecordList = list()
    files = findFilesInFolder(r"C:\imgTest",list(),"jpg",False)[0]
    imgs = [open(f , 'rb').read() for f in files]
    for img in imgs:
        imageRecordList.append(ImageRecord(str(uuid4()),round(datetime.now().microsecond),1,0.5,str(b64encode(img))))

    return imageRecordList


def produce_object_detections(conn, table, coord_type, max_objects=9999,
                              num_plot=9999, fig_size=None):
    '''
    Plot images with drawn bounding boxes.
    conn : CAS
        CAS connection object
    table : string or CASTable
        Specifies the object detection castable to be plotted.
    coord_type : string
        Specifies coordinate type of input table
    max_objects : int, optional
        Specifies the maximum number of bounding boxes to be plotted on an image.
        Default: 10
    num_plot : int, optional
        Specifies the name of the castable.
    n_col : int, optional
        Specifies the number of column to plot.
        Default: 2
    fig_size : int, optional
        Specifies the size of figure.
    '''
    conn.retrieve('loadactionset', _messagelevel = 'error', actionset = 'image')

    input_tbl_opts = input_table_check(table)
    input_table = conn.CASTable(**input_tbl_opts)
    img_num = input_table.shape[0]
    num_plot = num_plot if num_plot < img_num else img_num
    input_table = input_table.sample(num_plot)
    det_label_image_table = random_name('detLabelImageTable')

    num_max_obj = input_table['_nObjects_'].max()
    max_objects = max_objects if num_max_obj > max_objects else num_max_obj

    with sw.option_context(print_messages=False):
        res = conn.image.extractdetectedobjects(casout = {'name': det_label_image_table, 'replace': True},
                                                coordtype=coord_type,
                                                maxobjects=max_objects,
                                                table=input_table)
        if res.severity > 0:
            for msg in res.messages:
                print(msg)

    outtable = conn.CASTable( det_label_image_table)
    imageRecordList = list()
    in_df = input_table.fetch()['Fetch']
    out_df = outtable.fetch()['Fetch']

    if len(out_df) == len(in_df):
        print(str(len(out_df)) + " equal table length assumption is met, producing message buffer")
        for i in range(len(out_df)):
            imageId = str(uuid4())
            timestamp = round(datetime.now().microsecond)
            nbrOfBoats = int(in_df['_nObjects_'][i])
            imgStr = out_df['_image_'][i]
            nparr = np.frombuffer(imgStr, np.uint8)
            #img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            base_img = str(base64.b64encode(nparr))

            occupancy_rate = 0
            if nbrOfBoats > 0:
                surface_list = list()
                index = 5
                for ix in range(nbrOfBoats):
                    surface_list.append(in_df.iloc[i,index+4]*in_df.iloc[i,index+5])
                    index = index + 6
                occupancy_rate = sum(surface_list)

            imageRecordList.append(ImageRecord(imageId,timestamp,nbrOfBoats,occupancy_rate,base_img))


    with sw.option_context(print_messages=False):
        conn.table.droptable(det_label_image_table)

    return imageRecordList