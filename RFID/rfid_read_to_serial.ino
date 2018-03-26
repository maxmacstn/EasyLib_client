#include <SPI.h>
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 9
MFRC522 mfrc522(SS_PIN, RST_PIN);   // Create MFRC522 instance.
String content = "";
unsigned long lastScanTime = 0;

void setup() 
{
  Serial.begin(9600);   // Initiate a serial communication
  SPI.begin();      // Initiate  SPI bus
  mfrc522.PCD_Init();   // Initiate MFRC522
  //mfrc522.PCD_WriteRegister(0x26, (0x07<<4)); // Set Rx Gain to max
  mfrc522.PCD_SetAntennaGain(mfrc522.RxGain_max);
  Serial.println("Put your card to the reader...");
  Serial.println();
 
}
void loop() 
{
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent()) 
  {
    return;
  }
  // Select one of the cards
  if ( ! mfrc522.PICC_ReadCardSerial()) 
  {
    return;
  }

  //Show UID on serial monitor
  String newContent= "";
  byte letter;
  for (byte i = 0; i < mfrc522.uid.size; i++) 
  {
     //Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
     //Serial.print(mfrc522.uid.uidByte[i], HEX);
     newContent.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : ""));
     newContent.concat(String(mfrc522.uid.uidByte[i], HEX));
  }

  //Check is the same card within 5 seconds
  if (newContent == content && millis() - lastScanTime < 5000 ){
    return;
  }
  lastScanTime = millis();
  content = newContent;
  Serial.println(content);
} 
