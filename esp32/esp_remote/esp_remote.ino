/*
 * Author: Jitesh Saini
 * Website: https://helloworld.co.in
 * 
 * This code works with Online Web Remote available at https://helloworld.co.in/iot/remote
 * Using the Web Remote you can send GPIO toggle requests to the helloworld server. 
 * This esp32 code fetches the toggle request from your account in helloworld server and set the GPIO as selected by Web Remote.
 *
 * The program does following:-
 *  - Auto connects to wifi
 *  - checks data on the server every 20 seconds and fetch data
 *  (The GPIO pins configured on web remote will be controlled automatically, no need to change the code here)
 */
 
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YourSSID";
const char* password = "YourPassword";

String auth_token = "xxxx"; //paste your auth_token here
String board_no = "board_1"; 

/***********************************************************************************/
/******************DO NOT MODIFY THE CODE BELOW*************************************/
/***********************************************************************************/

String server = "https://helloworld.co.in/iot/remote/read_data.php";

#define builtIn_Led 2
unsigned int flag_timer_interrupt = 0;
hw_timer_t * timer = NULL;
DynamicJsonDocument doc(1024);

//Timer interrupt function
void IRAM_ATTR onTimer() {
 //Serial.println("Timer Interrupt Function");
 flag_timer_interrupt=1;
}

void setup_wifi(){
  delay(50);
  Serial.println();
  Serial.println("Connecting to WiFi");
  
  WiFi.begin(ssid, password);

  int c=0;
  while (WiFi.status() != WL_CONNECTED) {
    blink_led(2); //blink LED twice to indicate that wifi not connected
    delay(1000); //
    Serial.print(".");
    c=c+1;
    if(c>10){
        ESP.restart(); //restart ESP after 10 seconds if not connected to wifi
    }
  }
  Serial.println("");
  Serial.print("connected to Wifi with IP address: ");
  Serial.println(WiFi.localIP());
}

void setup() {
  Serial.begin(115200); 
  pinMode(builtIn_Led, OUTPUT);
  
  setup_wifi();
  
  unsigned int interrupt_dur = 20;
  timer = timerBegin(0, 80, true);
  timerAttachInterrupt(timer, &onTimer, true);
  timerAlarmWrite(timer, interrupt_dur*1000000, true); //1000000 is one second
  timerAlarmEnable(timer);

  fetch_data("1");
}

void blink_led(unsigned int n){
  for (int i = 0; i < n; i++) {
    digitalWrite(builtIn_Led, HIGH);
    delay(200);
    digitalWrite(builtIn_Led, LOW); 
    delay(200);
  }
}

void set_pin_state(String pin_no, String state){
  pinMode(pin_no.toInt(), OUTPUT);      // set the pin mode
  digitalWrite(pin_no.toInt(), state.toInt());
}

void fetch_data(char* zz)
{
   //zz=="1" on boot request, server sends all the data 
   //zz=="0" regular request, server sends the changes only
   
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      
      String serverPath = server + "?p="+ auth_token + "*" + board_no + "*esp" + "*" + zz;
      Serial.println("");
      Serial.println(serverPath);
      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());
      
      // Send HTTP GET request
      int httpResponseCode = http.GET();
      
      if (httpResponseCode==200) {
        Serial.print("Success!!! HTTP Response code from Server: ");
        Serial.println(httpResponseCode);Serial.println("");
        String payload = http.getString(); //this variable stores the json data returned by the server. The high and low level triggers set on the widget are contained in it.
        
        Serial.println(payload);
        
        deserializeJson(doc, payload);
        JsonObject obj = doc.as<JsonObject>();
        
        for (JsonPair kv : obj) {
            Serial.print(kv.key().c_str());
            Serial.print(" : ");
            Serial.println(kv.value().as<char*>());

            set_pin_state(kv.key().c_str(),kv.value().as<char*>());
        }  
      }
      else {
        Serial.print("Server not reachable. Error code: ");
        Serial.println(httpResponseCode);
        blink_led(3); //blink the built-in led thrice to show server error
      }
      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
}

void loop() {
  //this flag is set inside the timer interrup function.
  while(flag_timer_interrupt==0){
    Serial.print("-");
    delay(1000);
    if(WiFi.status()!= WL_CONNECTED){
      Serial.println("WiFi Disconnected, Re-connecting..");
      setup_wifi();
    }
  }
  flag_timer_interrupt=0;

  fetch_data("0");
  
}
