import java.io.FileWriter
import java.time.LocalDateTime
import java.util
import java.util.Map

import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import org.apache.http.client.entity.UrlEncodedFormEntity
import org.apache.http.client.methods.{CloseableHttpResponse, HttpGet, HttpPost}
import org.apache.http.client.params.{CookiePolicy, HttpClientParams}
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.{BasicResponseHandler, DefaultHttpClient}
import org.apache.http.message.BasicNameValuePair
import org.apache.http.protocol.HTTP
import org.apache.http.util.EntityUtils
import spray.json._

object OathConnectAPI extends JsonUtils {


  case class OathConfig(
                         loginHost: String = null,
                         username: String = null,
                         password: String = null,
                         client_id: String = null,
                         client_secret: String = null,
                         access_token: String = null,
                         clientIdEndpoint: String = null
                       ) {
    def getSalesForceDefault: OathConfig = {
      OathConfig(loginHost = "https://eu16.salesforce.com/",
        username = "username",
        //use your password+your secret token (eg passwordToken)
        password = "pp",
        client_id = "clientid",
        client_secret = "clientSecret")
    }

  }


  def oAuthClient(oathConfig: OathConfig = new OathConfig().getSalesForceDefault): OathConfig = {
    val client = new DefaultHttpClient()
    val params = client.getParams
    HttpClientParams.setCookiePolicy(params, CookiePolicy.BEST_MATCH)
    params.setParameter("CONNECTION_TIMEOUT", 30000)
    val baseUrl = oathConfig.loginHost + "/services/oauth2/token"
    val parametersBody = new util.ArrayList[BasicNameValuePair]
    parametersBody.add(new BasicNameValuePair("grant_type", "password"))
    parametersBody.add(new BasicNameValuePair("username", oathConfig.username))
    parametersBody.add(new BasicNameValuePair("password", oathConfig.password))
    parametersBody.add(new BasicNameValuePair("client_id", oathConfig.client_id))
    parametersBody.add(new BasicNameValuePair("client_secret", oathConfig.client_secret))

    val oauthPost = new HttpPost(baseUrl)
    oauthPost.setEntity(new UrlEncodedFormEntity(parametersBody, HTTP.UTF_8))
    val response: CloseableHttpResponse = client.execute(oauthPost)
    val code = response.getStatusLine.getStatusCode // use code to refresh the api
    val oauthLoginResponse: Map[String, String] = new Gson().fromJson(EntityUtils.toString(response.getEntity), new TypeToken[util.HashMap[String, String]]() {}.getType)
    OathConfig(loginHost = oathConfig.loginHost,
      username = oathConfig.username,
      password = oathConfig.password,
      client_id = oathConfig.client_id,
      client_secret = oathConfig.client_secret,
      access_token = oauthLoginResponse.get("access_token"),
      clientIdEndpoint = oauthLoginResponse.get("id"))
  }


  def getRequest(apiUrl: String = "/services/data/v44.0/sobjects/",
                 sObject: String = null, objectId: String = null,
                 oathConfig: OathConfig): String = {

    val access_token = oathConfig.access_token
    val url = oathConfig.loginHost + apiUrl
    val request = new HttpGet(url)

    request.addHeader("Authorization", "Bearer " + access_token)
    request.addHeader("Content-type", "application/json")
    val client = new DefaultHttpClient
    val response = client.execute(request)
    val handler = new BasicResponseHandler()
    val body = handler.handleResponse(response)
    return body
  }

  def postRequest(apiUrl: String = "/services/data/v44.0/sobjects/",
                  sobject: String = null,
                  jsonData: String = null,
                  oathConfig: OathConfig): Unit = {

    val url = oathConfig.loginHost + apiUrl + sobject
    println(s"This is the url: $url")
    val request = new HttpPost(url)
    request.addHeader("Authorization", "Bearer " + oathConfig.access_token)
    request.addHeader("Content-type", "application/json")
    request.setEntity(new StringEntity(jsonData))

    println(jsonData)
    println(request.toString)
    val client = new DefaultHttpClient
    val response = client.execute(request)
    val handler = new BasicResponseHandler()


    val body = handler.handleResponse(response).parseJson
    import PostMessageProtocol._
   val postMessage =   body.convertTo[PostMessage]
    val fw = new FileWriter("SalesforceOutput.csv", true) ;
    fw.write(s"${LocalDateTime.now()},${postMessage.postMessageToString}\n") ;
    fw.close()
  }



}
