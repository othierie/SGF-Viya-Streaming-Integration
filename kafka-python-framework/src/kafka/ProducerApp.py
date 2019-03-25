from confluent_kafka.avro import AvroProducer

from kafka.core.KafkaApp import KafkaApp


class ProducerApp(KafkaApp):

    def __init__(self, kafkaparameters, avroSchema,topic):
        super().__init__(kafkaparameters, avroSchema,topic)




    def produce(self, preparedMessageArray):
        prodConf = self.producerConfig()
        producer = AvroProducer(prodConf, default_value_schema=self.avroSchema)
        for preparedMessage in preparedMessageArray:

            producer.produce(topic=self.getTopic(), value=preparedMessage.to_dict(),
                             callback=lambda err, msg, obj=preparedMessage: self.on_delivery(err, msg, obj))
        producer.flush()







