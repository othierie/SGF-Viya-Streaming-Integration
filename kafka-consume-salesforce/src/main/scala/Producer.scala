
import java.util.Properties

import org.apache.avro.Schema
import org.apache.avro.generic.{GenericRecord, GenericRecordBuilder}
import org.apache.kafka.clients.producer.{KafkaProducer, ProducerRecord}
import org.apache.avro.Schema._

import scala.reflect.io.File





object Producer extends App {
  //GET SCHEMA FROM SCHEMA REGISTRY
  def get(url: String) = scala.io.Source.fromURL(url).mkString


  val props = new Properties()

  props.put("bootstrap.servers", KafkaParameters.KAFKA_BROKERS)
  props.put("key.serializer", KafkaParameters.KEY_SERIALIZER)
  props.put("value.serializer", KafkaParameters.MESSAGE_AVRO_SERIALIZER)
  props.put("schema.registry.url", KafkaParameters.SCHEMA_URL)
  props.put("acks", KafkaParameters.ACKS_POLICY)


  //record builder
  val fileStream = getClass.getResourceAsStream("basicavro/Payment.avsc")
  val schema = new Schema.Parser().parse(fileStream)
  val avroPayment = new GenericRecordBuilder(schema) {
    set("id", "paymentid2")
    set("amount" , 1.0)
  }.build()



  val producer = new KafkaProducer[String, GenericRecord](props)

  // val producer = new KafkaProducer[String, String](props)
  //producer.send(new ProducerRecord[String,String]("test1" ,  "ik ben ook een string"))
  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  producer.send(new ProducerRecord[String, GenericRecord](KafkaParameters.TEST_TOPIC_NAME, avroPayment))
  //  //producer.flush
  producer.close











}