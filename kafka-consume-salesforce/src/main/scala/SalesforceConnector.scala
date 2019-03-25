import java.util
import java.util.Properties

import org.apache.avro.generic.GenericRecord
import org.apache.kafka.clients.consumer.{ConsumerRecords, KafkaConsumer}
import spray.json._

class SalesforceConnector extends JsonUtils {


  //Set Kafka Properties
  val props = new Properties()
  props.put("bootstrap.servers", KafkaParameters.KAFKA_BROKERS)
  props.put("schema.registry.url", KafkaParameters.SCHEMA_URL)
  props.put("group.id", KafkaParameters.GROUP_ID)
  props.put("key.deserializer", KafkaParameters.KEY_DESERIALIZER)
  props.put("value.deserializer", KafkaParameters.MESSAGE_AVRO_DESERIALIZER)
  props.put("acks", KafkaParameters.ACKS_POLICY)

  //Start a REST session
  val oathConfig = OathConnectAPI.OathConfig().getSalesForceDefault
  val oathCreds = OathConnectAPI.oAuthClient()

  //Start The Consumer
  def salesForceConsumer(): Unit = {
    val consumer = new KafkaConsumer[String, GenericRecord](props)
    //subscribe to producer's topic
    consumer.subscribe(util.Arrays.asList(KafkaParameters.DELOITTE_KAFKA_TOPIC))
    var counter: Integer = 0
    //poll for new messages every two seconds
    //while (counter < 10) {
    while(true) {
      val records: ConsumerRecords[String, GenericRecord] = consumer.poll(2000)
      println(s"message count: ${records.count()}")
      //print each received record
      import scala.collection.JavaConversions._
      for (record <- records.iterator()) {

        //println(s"Here's your ${record.value()}")
        import DeloitteKafkaProtocol._

        val jsonTransaction = DeloitteKafka(record.value.get("imageId").toString, record.value.get("timestamp").asInstanceOf[Long], record.value.get("numOfBoats").asInstanceOf[Int], record.value.get("occupancyRate").asInstanceOf[Double]).toJson.toString()
        OathConnectAPI.postRequest("services/data/v44.0/sobjects/", "Kafka_Salesforce__c", jsonTransaction, oathCreds)

      }
      //commit offsets on last poll
      consumer.commitSync()
      counter = counter + 1
      println(counter)
    }
  }






}
object SalesforceConnector extends App {
  val sfc = new SalesforceConnector
  sfc.salesForceConsumer

}