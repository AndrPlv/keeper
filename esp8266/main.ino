#include <ArduinoJson.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 2   // Твой D4
#define RST_PIN 0  // Не подключай физически
#define LED 4 // сигнальный светодиод

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool cardWasRead = false; // Флаг, чтобы не спамило
const char* ssid = "andrecti";
const char* password = "Andrecti42.ru";

void setup() {
  Serial.begin(9600);  
  WiFi.begin(ssid, password);
  while (WiFi.status() !=  WL_CONNECTED) {
    Serial.println(WiFi.status());
    delay(500);
  }
  digitalWrite(LED, LOW);
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Поднеси карту...");
}

void loop() {
  // 1. Если карты нет — сбрасываем флаг
  if (!mfrc522.PICC_IsNewCardPresent()) {
    cardWasRead = false;
    return;
  }

  // 2. Если карта есть, но мы её уже читали — ничего не делаем
  if (cardWasRead) {
    return;
  }

  // 3. Пытаемся прочитать UID
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }

  String uidString = "";  
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    if (mfrc522.uid.uidByte[i] < 0x10) uidString += "0";
    uidString += String(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.print("ID карты:");
  Serial.println(uidString);
  if(Serial.available() > 0) {
    String input = Serial.readStringUntil('\n'); 
    input.trim();

    int separatorIndex = input.indexOf(':');

    if (separatorIndex != -1) {
      String part1 = input.substring(0, separatorIndex);
      String part2 = input.substring(separatorIndex + 1);
      send_info("password", uidString, part1, part2, "add");
      cardWasRead = true;
  }
  }
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();


  if (WiFi.status() !=  WL_CONNECTED) {
    digitalWrite(LED, LOW);
  }
  else {
    digitalWrite(LED, HIGH);
  }
}

int send_info(String password, String uid, String NameUser, String Group, String act) {
  HTTPClient http;
  WiFiClient me;
  http.begin(me, "http://10.154.158.91:5000/edit_user_list");
  http.addHeader("Content-Type", "application/json");

  DynamicJsonDocument doc(512);
  doc["password"] = password;
  doc["CardID"] = uid;
  doc["NameUser"] = NameUser;
  doc["Group"] = Group;
  doc["Time"] = "2026-10-24 18:10:00";
  doc["act"] = act;

  String json;
  serializeJson(doc, json);
  
  int code = http.POST(json);
  Serial.print("Возратный код: ");
  Serial.println(code);
  http.end();
  return code;
}
