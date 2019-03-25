from base64 import b64encode

import cv2
from datetime import datetime
import os
from uuid import uuid4
from dlpy.images import *
from dlpy.utils import display_object_detections

from dataUtils.avroUtils import ImageRecord

path = os.getcwd()

from swat import *
from dlpy.applications import *

def getImageRecordsViya():
    s= CAS('54.203.183.131',5570,'viyademo01','demopw')
    s.loadactionset('image')
    s.loadactionset('deepLearn')

    s.table.addcaslib(activeonadd=False,datasource={'srctype':'path'},
                     name='dnfs',path='/data/Poa/',subdirectories=True)



    anchors=(23.461414868105507, 18.062330935251786, 6.302249999999996, 4.3697777777777755, 13.978019911504417, 6.535996066863321, 2.74937962962963, 3.153810699588476, 3.899717391304346, 5.637603864734299)

    yolo_model = Tiny_YoloV2(s,
                            n_classes=1,
                            predictions_per_grid=5,
                            anchors = anchors,
                            max_boxes=100,
                            coord_type='coco',
                            max_label_per_image = 10,
                            class_scale=1.0,
                            coord_scale=1.0,
                            prediction_not_a_object_scale=1,
                            object_scale=5,
                            detection_threshold=0.1,
                            iou_threshold=0.1)


    #build model
    yolo_model.from_sashdat(s,path='/data/Poa/Tiny-Yolov2.sashdat')
    #yolo_model.load_weights(s,path='/opt/sasinside/DemoData/testdata/TYolo.sashdat.sashdat')
    #load test set
    s.plot_obj_det_image
    testSetTbl = ImageTable.load_files(conn=s, caslib='dnfs', path='/data/Poa/testset/')
    testSetTbl.resize(height=416, width=416, inplace=True)
    #yolo_model.predict(data=testSetTbl,layer_out='detections')
    sres= s.dlscore(
        model='Tiny-yolov2',        # CAS Table containing Model DAG
        randommutation='none',          # Not using random mutation to the input image
        initWeights='Tiny-Yolov2_weights',   # CAS Table containing the weights used to do the scoring
        table = testSetTbl,             # CAS Table containing the testing images
        copyVars=['_image_','_label_','_id_'], # CAS Table columns copied to the output table by the action
        nThreads=64,
        casout={'name':'detections', 'replace':True}  # CAS Table to save the detection output
    )

    #To turn castable to DF
    results=s.CASTable('detections')
    df=results.fetch()
    imgBuffer = list()
    for i in range(len(df['Fetch']['_image_'])):
        image = df['Fetch']['_image_'][i]
        nparr = np.frombuffer(image, dtype=np.uint8)
        mg_np = str(cv2.imdecode(nparr, cv2.IMREAD_COLOR))
        producerImage = str(b64encode(nparr))
        imgBuffer.append(ImageRecord(str(uuid4()),round(datetime.now().microsecond),1,0.5,producerImage))

    return imgBuffer



