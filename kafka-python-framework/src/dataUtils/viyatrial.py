#coding: utf-8

# # DLPy code for training and scoring a YoloV2 model on SAS Viya

# In[1]:
import h5py
from frontend import YOLO
import os
path = os.getcwd()
print(path)


# In[ ]:


#import required libraries
from swat import *
import swat as sw
from pprint import pprint
import matplotlib
import sys
import dlpy
from dlpy.utils import *
from dlpy.model import *
from dlpy.applications import *
import onnxmltools
onnxmltools.convert_keras
# In[ ]:




from dlpy.model import *
from dlpy.applications import *
# Connect to a CAS sever
s= CAS('54.203.183.131',5570,'viyademo01','demopw')

s.loadactionset('image')
s.loadactionset('deepLearn')
s.sessionprop.setsessopt(timeout=31536000)

# In[ ]:


#uploading the 8000+ images and corresponding label file to a sas table
#labelling was done using the coco coordinate type (min/max)
object_detection_targets = create_object_detection_table(s,
                                                         data_path = '/data/Poa/labelled_images',
                                                         coord_type = 'yolo',
                                                         output = 'ImageDataSet',
                                                         )


# In[ ]:


#get back number of images processed
s.numrows('ImageDataSet')
#K-means procedure to find initial anchors

anchors=get_anchors(s,data='ImageDataSet',n_anchors=4, coord_type='yolo')
#assigning a CAS library
s.table.addcaslib(activeonadd=False,datasource={'srctype':'path'},
                  name='dnfs',path=path,subdirectories=True)
print(path)
#initialize the target and input tables
targets = ['_nObjects_'];
for i in range(0,1):
    targets.append('_Object%d_'%i)
    for sp in ["xmin", "xmax", "ymin", "ymax"]:
        targets.append ('_Object%d_%s'%(i, sp))

inputVars = []
inputVars.insert(0, '_image_')

#set up YoloV2 architecture
yolo_model = YoloV2(s,
                    n_classes=2,
                    predictions_per_grid=4,
                    anchors = anchors,
                    max_boxes=100,
                    coord_type='coco',
                    max_label_per_image = 100,
                    class_scale=1.0,
                    coord_scale=1.0,
                    prediction_not_a_object_scale=1,
                    object_scale=5,
                    detection_threshold=0.2,
                    iou_threshold=0.2)


# In[ ]:


#load existing weights to kickstart the learning process
#s.table.loadtable(casout={'name':'TYolov2_weights','replace':True},
#                  caslib='dnfs',
#                  path="Tiny-Yolov2_weights.sashdat");


# In[ ]:


#set parameters for training
solver = MomentumSolver(learning_rate=0.001, clip_grad_max = 100, clip_grad_min = -100)
optimizer = Optimizer(algorithm=solver, mini_batch_size=64, log_level=2, max_epochs=1, reg_l2=0.005)
data_specs = [DataSpec(type_='IMAGE', layer='Input1', data=inputVars),
              DataSpec(type_='OBJECTDETECTION', layer='Detection1', data=targets)]
#set initial weights
#yolo_model.set_weights('TYolov2_weights')
#train model
yolo_model.fit(data='ImageDataSet',
               optimizer=optimizer,
               data_specs=data_specs,
               n_threads=64,
               record_seed=13309,
               force_equal_padding=True)


# In[ ]:

yolo_model.save_to_table(path='/data/Poa')


#save weights to a sas table
s.save('Yolov2_weights',name='Weights_yoloV2',caslib='dnfs',replace=True)

