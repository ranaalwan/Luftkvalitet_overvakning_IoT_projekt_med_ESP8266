#include "MQ135.h"
#include <ESP8266WiFi.h>

#define D5 14
#define D6 12
#define D7 13

String apiKey = "JUVRZNJWQOWXH8O2"; // Enter your Write API key from ThingSpeak
const char *ssid = "wifi ssid";   // replace with your WiFi SSID
const char *pass = "password";        // replace with your WiFi password
const char *server = "api.thingspeak.com";
const int sensorPin = 0;
int air_quality;

#define MQ2 A0
#define GREEN D5
#define RED D6
#define BUZZER D7


WiFiClient client;

void setup()
{
  Serial.begin(115200);
  delay(10);

  Serial.println("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  pinMode(GREEN, OUTPUT);
  pinMode(RED, OUTPUT);
  pinMode(BUZZER, OUTPUT);
}

void loop()
{
  MQ135 gasSensor = MQ135(A0);
  air_quality = gasSensor.getPPM();

  if (client.connect(server, 80))
  {
    String postStr = apiKey;
    postStr += "&field1=";
    postStr += String(air_quality);
    postStr += "\r\n\r\n";

    client.print("POST /update HTTP/1.1\n");
    client.print("Host: api.thingspeak.com\n");
    client.print("Connection: close\n");
    client.print("X-THINGSPEAKAPIKEY: " + apiKey + "\n");
    client.print("Content-Type: application/x-www-form-urlencoded\n");
    client.print("Content-Length: ");
    client.print(postStr.length());
    client.print("\n\n");
    client.print(postStr);

    Serial.print("Air Quality: ");
    Serial.print(air_quality);
    Serial.println(" PPM. Sent to ThingSpeak.");

    // Control LED and Buzzer based on air quality level
    if (air_quality > 1000)
    {
      digitalWrite(GREEN, LOW);
      digitalWrite(RED, HIGH);
      digitalWrite(BUZZER, HIGH);
      Serial.println("Det finns gas här..");
      delay(300);

    }
    else
    {
      digitalWrite(GREEN, HIGH);
      digitalWrite(RED, LOW);
      digitalWrite(BUZZER, LOW);
    }
  }

  client.stop();

  Serial.println("Waiting...");

  // ThingSpeak needs a minimum 2 sec delay between updates
  delay(2000);
}
