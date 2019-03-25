#coding: utf-8

# # DLPy code for training and scoring a YoloV2 model on SAS Viya

# In[1]:


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


# In[ ]:


from dlpy.model import *
from dlpy.applications import *
# Connect to a CAS sever
s= CAS('54.203.183.131',5570,'viyademo01','demopw')

s.loadactionset('image')
s.loadactionset('deepLearn')
s.sessionprop.setsessopt(timeout=31536000)
s.close()