

import java.util
import java.util.Properties

import org.apache.avro.Schema
import org.apache.avro.generic.GenericRecord
import org.apache.kafka.clients.consumer.{ConsumerRecord, ConsumerRecords, KafkaConsumer}

import scala.collection.mutable.ArrayBuffer




object Consumer extends App {
  //get kafka url and registry url or use default if not specified
  val props = new Properties()

  props.put("bootstrap.servers", KafkaParameters.KAFKA_BROKERS)
  props.put("schema.registry.url", KafkaParameters.SCHEMA_URL)
  props.put("group.id", KafkaParameters.GROUP_ID)
  props.put("key.deserializer", KafkaParameters.KEY_DESERIALIZER)
  props.put("value.deserializer", KafkaParameters.MESSAGE_AVRO_DESERIALIZER)
  props.put("acks", KafkaParameters.ACKS_POLICY)


  //create new consumer
  val consumer = new  KafkaConsumer[String, GenericRecord](props)
  //subscribe to producer's topic
  consumer.subscribe(util.Arrays.asList(KafkaParameters.TEST_TOPIC_NAME))

  //poll for new messages every two seconds
  while(true) {
    val records: ConsumerRecords[String, GenericRecord] = consumer.poll(2000)
    println(s"message count: ${records.count()}")
    //print each received record
    import scala.collection.JavaConversions._
    for (record <- records.iterator()) {

      println(s"Here's your ${record.value()}")
    }

    //commit offsets on last poll
    consumer.commitSync()
  }

}