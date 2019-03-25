This Repo contains the code used for SAS Paper 3725: Embracing the open API ecosystem to give analytics an organizational operational landing spot
The goal of this repo is to provide the reader with examples about how we made the proof of conncept work. I took out all ip addresses and user-connection
information, so if you want to make this work, you will have to put your own details there

You need the following instances:
 Salesforce Cloud environment: https://eu16.salesforce.com
 Running SAP Hana instance on https://account.hanatrial.ondemand.com
 Kafka Cluster running on aws or somewhere else
 SAS VIYA on 

kafka-consume-salesforce:
  contains code to consume message from a kafka and push them to salesforce by using the REST api
 
flask-video-streaming-master-SGF:
  contains code to read pictures from a directory and feed them to a flask app
  The code is an extention on miguelgrinberg's project, I only created a class with some threads in order to feed his app
  https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited
  https://github.com/miguelgrinberg/flask-video-streaming
 
 Jupyter notebooks:
  Contains two ipython notebook, one will show you how we check values in our Hana trial instance, the other contains the code of training
  the yolov2 model on 8000 labelled pictures
  
  Kafka-python-framework:
    Contains a tiny framework in order to produce and consume kafka messages, you can also find the Viya Producer here


