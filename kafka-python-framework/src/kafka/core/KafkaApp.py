#Initiates the Kafka app, by setting general kafka.config

class KafkaApp(object):
    def __init__(self, kafkaparameters, avroSchema,topic):
        self.kafkaParameters = kafkaparameters
        self.avroSchema = avroSchema
        self.topic = topic

    def getTopic(self):
        if self.topic == "test":
            return self.kafkaParameters.TEST_TOPIC_NAME
        else:
            return self.kafkaParameters.DELOITTE_KAFKA_TOPIC
        
    def producerConfig(self):
        conf = {'bootstrap.servers': self.kafkaParameters.KAFKA_BROKERS,
                'schema.registry.url': self.kafkaParameters.SCHEMA_URL}
        return conf
    
    def consumerConfig(self):
        conf = {'bootstrap.servers': self.kafkaParameters.KAFKA_BROKERS,
                'schema.registry.url': self.kafkaParameters.SCHEMA_URL,
                'group.id': self.kafkaParameters.GROUP_ID,
                'auto.offset.reset': self.kafkaParameters.CONSUMER_POLICY}
        return conf

    def on_delivery(self,err, msg, obj):
        """
            Handle delivery reports served from producer.poll.
            This callback takes an extra argument, obj.
            This allows the original contents to be included for debugging purposes.
        """
        if err is not None:
            print('Message {} delivery failed for user {} with error {}'.format(
                obj.id, obj.name, err))
        else:
            print('Message {} successfully produced to {} [{}] at offset {}'.format(
                obj.id, msg.topic(), msg.partition(), msg.offset()))
