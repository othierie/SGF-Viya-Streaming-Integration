class KafkaParameters(object):
    def __init__(self, KAFKA_BROKERS, ZOOKEEPER, SCHEMA_URL, TEST_TOPIC_NAME,DELOITTE_KAFKA_TOPIC, GROUP_ID, KEY_SERIALIZER,KEY_DESERIALIZER,MESSAGE_STRING_SERIALIZER,MESSAGE_STRING_DESERIALIZER,MESSAGE_AVRO_SERIALIZER,MESSAGE_AVRO_DESERIALIZER,ACKS_POLICY,CONSUMER_POLICY,SAP_TOPIC ):
        self.KAFKA_BROKERS = KAFKA_BROKERS
        self.ZOOKEEPER = ZOOKEEPER
        self.SCHEMA_URL = SCHEMA_URL
        self.TEST_TOPIC_NAME = TEST_TOPIC_NAME
        self.DELOITTE_KAFKA_TOPIC = DELOITTE_KAFKA_TOPIC
        self.GROUP_ID = GROUP_ID
        self.KEY_SERIALIZER = KEY_SERIALIZER
        self.KEY_DESERIALIZER = KEY_DESERIALIZER
        self.MESSAGE_STRING_SERIALIZER = MESSAGE_STRING_SERIALIZER
        self.MESSAGE_STRING_DESERIALIZER = MESSAGE_STRING_DESERIALIZER
        self.MESSAGE_AVRO_SERIALIZER = MESSAGE_AVRO_SERIALIZER
        self.MESSAGE_AVRO_DESERIALIZER = MESSAGE_AVRO_DESERIALIZER
        self.ACKS_POLICY = ACKS_POLICY
        self.CONSUMER_POLICY = CONSUMER_POLICY
        self.SAP_TOPIC = SAP_TOPIC

    def __init__(self):
        self.KAFKA_BROKERS = 'xx.xxx.xxx.xxx:9092'
        self.ZOOKEEPER = 'xx.xxx.xxx.xxx:2181'
        self.SCHEMA_URL =  'http://xx.xxx.xxx.xxx:8080'
        self.TEST_TOPIC_NAME = 'userTest'
        self.DELOITTE_KAFKA_TOPIC = 'deloitteKafka'
        self.GROUP_ID = 'pythonGroup'
        self.KEY_SERIALIZER = 'org.apache.kafka.common.serialization.StringSerializer'
        self.KEY_DESERIALIZER = 'org.apache.kafka.common.serialization.StringDeserializer'
        self.MESSAGE_STRING_SERIALIZER = 'org.apache.kafka.common.serialization.StringSerializer'
        self.MESSAGE_STRING_DESERIALIZER = 'org.apache.kafka.common.serialization.StringDeserializer'
        self.MESSAGE_AVRO_SERIALIZER = 'io.confluent.kafka.serializers.KafkaAvroSerializer'
        self.MESSAGE_AVRO_DESERIALIZER = 'io.confluent.kafka.serializers.KafkaAvroDeserializer'
        self.ACKS_POLICY = 'all'
        self.CONSUMER_POLICY = 'earliest'
        self.SAP_TOPIC = 'sapKafka'





