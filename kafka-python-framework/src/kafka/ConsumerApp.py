import json
import random
import uuid

from collections import namedtuple

from confluent_kafka.avro import AvroConsumer, SerializerError

from dataUtils.ReadImage import  writeImageToDisk
from kafka.core.KafkaApp import KafkaApp


class ConsumerApp(KafkaApp):

    def __init__(self, kafkaparameters, avroSchema,topic, consumedObjectName):
        super().__init__(kafkaparameters, avroSchema,topic)
        self.consumedObjectName = consumedObjectName


    def consumeImageToDir(self):
        consConf = self.consumerConfig()
        consumer = AvroConsumer(consConf)
        consumer.subscribe([self.getTopic()])
        counter = 0
        while True :

            try:
                msg = consumer.poll(1)

                # There were no messages on the queue, continue polling
                if msg is None:
                    continue

                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue

                record =  json.loads(json.dumps(msg.value()), object_hook=lambda d: namedtuple(self.consumedObjectName, d.keys())(*d.values()))
                counter +=1
                print("processed {} messages".format(counter))
                #print(record)

                #adapt the path!
                writeImageToDisk(record.image, r"enter the directory here" + str(record.imageId)+".jpg")


            except SerializerError as e:
                # Report malformed record, discard results, continue polling
                print("Message deserialization failed {}".format(e))
                continue
            except KeyboardInterrupt:
                break

        print("Shutting down consumer..")
        consumer.close()


    def consumeToList(self):
        consConf = self.consumerConfig()
        consumer = AvroConsumer(consConf)
        consumer.subscribe([self.getTopic()])

        messageList = list()
        i = 0
        while i < 20 :
            print(i)
            i += 1
            try:
                msg = consumer.poll(1)

                # There were no messages on the queue, continue polling
                if msg is None:
                    continue

                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                    continue
                record = json.loads(json.dumps(msg.value()), object_hook=lambda d: namedtuple(self.consumedObjectName, d.keys())(*d.values()))
                messageList.append(record)
            except SerializerError as e:
                # Report malformed record, discard results, continue polling
                print("Message deserialization failed {}".format(e))
                continue
            except KeyboardInterrupt:
                break

        print("Shutting down consumer..")
        consumer.close()
        return messageList

