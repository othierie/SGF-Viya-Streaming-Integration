import base64
from datetime import datetime
from uuid import uuid4

import numpy as np
# sys.path.append(dlpy_path)
from dlpy.applications import *
from dlpy.images import ImageTable
from dlpy.utils import *
from dlpy.utils import input_table_check, random_name
from swat import *

from dataUtils.avroUtils import ImageRecord, deloitte_kafka_schema
from kafka.ProducerApp import ProducerApp
from kafka.config.KafkaParameters import KafkaParameters


def viyaStartUp():
    s= CAS('xx.xxx.xxx.xxx',5570,'viyademo01','demopw')
    s.loadactionset('image')
    s.loadactionset('deepLearn')
    model_load = Model(s)
    model_file = '/root/fullModel/Yolov2.sashdat'
    model_load.load(path=model_file)
    #test = ImageTable.load_files(conn=s, caslib='dnfs', path='/data/Poa/testData/labelled_images')
    test = ImageTable.load_files(conn=s, caslib='dnfs', path='/data/Poa/validation')
    test.resize(height=416, width=416, inplace=True)
    prd = model_load.predict(data=test)
    return [s,prd]

def getTableName(predict_model_object):
    return CASTable(predict_model_object.get('OutputCasTables').Name[0],coord_type='yolo')

def kafkaStartUp():
    return  ProducerApp(kafkaparameters=  KafkaParameters(), avroSchema=deloitte_kafka_schema, topic="kafka")


def produce_object_detections(conn, table, coord_type, producerApp):
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
    det_label_image_table = random_name('detLabelImageTable')
    num_max_obj = input_table['_nObjects_'].max()

    with sw.option_context(print_messages=False):
        res = conn.image.extractdetectedobjects(casout = {'name': det_label_image_table, 'replace': True},
                                                coordtype=coord_type,
                                                maxobjects=num_max_obj,
                                                table=input_table)
        if res.severity > 0:
            for msg in res.messages:
                print(msg)
    outtable = conn.CASTable( det_label_image_table)
    #imageRecordList = list()
    in_df = input_table.fetch()['Fetch']
    out_df = outtable.fetch()['Fetch']
    if len(out_df) == len(in_df):
        print(str(len(out_df)) + " equal table length assumption is met, producing message buffer")
        for i in range(len(out_df)):
            imageId = str(uuid4())
            t = datetime.now()
            timestamp = round((t-datetime(1970,1,1)).total_seconds())
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
                occupancy_rate = round(sum(surface_list),4)

            #imageRecordList.append(ImageRecord(imageId,timestamp,nbrOfBoats,occupancy_rate,base_img))
            producerApp.produce(preparedMessageArray= [ImageRecord(imageId,timestamp,nbrOfBoats,occupancy_rate,base_img)])

    with sw.option_context(print_messages=False):
        conn.table.droptable(det_label_image_table)

