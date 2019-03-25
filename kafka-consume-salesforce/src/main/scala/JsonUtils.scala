import spray.json._


trait JsonUtils {
  case class PostMessage(id: String, success: Boolean, error: Option[String] ){
    def postMessageToString(): String = {
      s"$id,$success,${error}"
    }
  }

  case class Transaction(name: String, amount__c: Double)
  case class Test(name:String)
  case class DeloitteKafka(imageId__c: String, timestamp__c: Long, numberOfBoats__c: Int, occupancyRate__c: Double)

  object TransactionProtocol extends DefaultJsonProtocol {
    implicit val transactionFormat = jsonFormat2(Transaction)
  }
  object PostMessageProtocol extends DefaultJsonProtocol {
    implicit val transactionFormat = jsonFormat3(PostMessage)
  }
  object TestProtocol extends DefaultJsonProtocol {
    implicit val transactionFormat = jsonFormat1(Test)
  }
  object DeloitteKafkaProtocol extends DefaultJsonProtocol {
    implicit val transactionFormat = jsonFormat4(DeloitteKafka)
  }
}




