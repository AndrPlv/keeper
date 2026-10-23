#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN 2   // Твой D4
#define RST_PIN 0  // Не подключай физически

MFRC522 mfrc522(SS_PIN, RST_PIN);

bool cardWasRead = false; // Флаг, чтобы не спамило
const char* ssid = "NameWiFi";
const char* password = "Wifipassword";

void setup() {
  Serial.begin(9600);
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

  // 4. ВЫВОДИМ ТОЛЬКО UID
  Serial.print("UID: ");
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    // Добавляем 0 перед числами меньше 16 (чтобы было 04, а не 4)
    if (mfrc522.uid.uidByte[i] < 0x10) {
      Serial.print("0");
    }
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println(); // Перенос строки

  // 5. Останавливаем карту и ставим флаг
  mfrc522.PICC_HaltA();
  mfrc522.PCD_StopCrypto1();
  cardWasRead = true;
}
