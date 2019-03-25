from dataUtils.avroUtils import deloitte_kafka_schema
from kafka.ConsumerApp import ConsumerApp
from kafka.config.KafkaParameters import KafkaParameters

def main():
    consumer = ConsumerApp(kafkaparameters=  KafkaParameters(), avroSchema=deloitte_kafka_schema, topic="kafka", consumedObjectName="ImageRecord", )
    consumer.consumeImageToDir()

if __name__ == '__main__':
    main()

