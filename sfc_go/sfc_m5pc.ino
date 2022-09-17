#include <M5StickCPlus.h>
#include <math.h>
#include <WiFi.h>
#include <WiFiMulti.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Adafruit_BMP280.h>
#include "SHT20.h"
#include "yunBoard.h"
#include "display.h"

// WiFi
WiFiClient client;

const char *ssid = "PDCN";
const char *password = "takoyaki123";

// YUN
SHT20 sht20;
Adafruit_BMP280 bmp;

uint32_t update_time = 0;
float tmp, hum;
float pressure;
uint16_t light;
extern uint8_t lightR;
extern uint8_t lightG;

uint8_t light_flag = 0;

const int capacity = JSON_OBJECT_SIZE(2);
StaticJsonDocument<capacity> json_request;
char buffer[255];

const char *host = "api.ami.moe/sfcgo";

unsigned long counter = 0;
unsigned long tick = 0;

void setup()
{
    int8_t i, j;
    M5.begin();
    M5.Axp.ScreenBreath(10);  // 画面の輝度を少し下げる
    M5.Lcd.setRotation(3);    // 左を上にする
    M5.Lcd.setTextSize(2);    // 文字サイズを2にする
    M5.Lcd.fillScreen(BLACK); // 背景を黒にする
    Wire.begin(0, 26, 100000UL);
    M5.Lcd.setRotation(1);
    M5.Lcd.setTextSize(2);

    // RGB888
    // led_set(uint8_t 1, 0x080808);

    if (!bmp.begin(0x76))
    {
        Serial.println(
            F("Could not find a valid BMP280 sensor, check wiring!"));
    }

    /* Default settings from datasheet. */
    bmp.setSampling(Adafruit_BMP280::MODE_NORMAL,      /* Operating Mode. */
                    Adafruit_BMP280::SAMPLING_X2,      /* Temp. oversampling */
                    Adafruit_BMP280::SAMPLING_X16,     /* Pressure oversampling */
                    Adafruit_BMP280::FILTER_X16,       /* Filtering. */
                    Adafruit_BMP280::STANDBY_MS_1000); /* Standby time. */

    // put your setup code here, to run once:
    display_light4();

    M5.Axp.ScreenBreath(9);
    M5.Lcd.setRotation(3);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setTextSize(2);

    M5.Lcd.println("[M5StickCP]");
    delay(1000);

    M5.Lcd.println("start Serial");
    Serial.begin(115200);
    while (!Serial)
        ;
    delay(100);

    M5.Lcd.println("start WiFi");
    Serial.print("start Wifi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        Serial.print(".");
        delay(100);
    }
    Serial.println("");
    M5.Lcd.println("Connected");
}

void loop()
{
    // led_set_all((lightR << 16) | (lightG << 8) | lightB);
    if (millis() > update_time) {
        update_time = millis() + 1000;
        tmp         = sht20.read_temperature();
        hum         = sht20.read_humidity();
        light       = light_get();
        pressure    = bmp.readPressure();
        M5.Lcd.setCursor(3, 3);
        M5.Lcd.setTextColor(TFT_BLUE, TFT_BLACK);
        M5.Lcd.print("YUN");
        M5.Lcd.setCursor(0, 25);
        M5.Lcd.setTextColor(TFT_RED, TFT_BLACK);
        M5.Lcd.printf("%.2fC\r\n", tmp);
        M5.Lcd.setCursor(0, 25 + 20);
        M5.Lcd.setTextColor(TFT_RED, TFT_BLACK);
        M5.Lcd.printf("%d", int(hum));
        M5.Lcd.print("%\r\n");
        M5.Lcd.setCursor(0, 25 + 20 + 20);
        M5.Lcd.setTextColor(TFT_RED, TFT_BLACK);
        M5.Lcd.printf("%d Pa\r\n", int(pressure));
        M5.Lcd.setCursor(0, 25 + 20 + 20 + 20);
        M5.Lcd.print("Wi-Fi:PDCN");
    }
    M5.update();

    if (M5.BtnA.wasPressed()) {
        esp_restart();
    }

    delay(10);
    // put your main code here, to run repeatedly:

    display_light();
    if (light > 1500) {
        if (light_flag == 0) {
            light_flag = 1;
            lightR     = 40;
            lightG     = 40;
        }
        led_breath();
    } else {
        led_off();
        light_flag = 0;
    }
    //wifi
    counter++;
    tick = millis();

    json_request["tmp"] = tmp;
    json_request["hum"] = hum;

    serializeJson(json_request, Serial);
    Serial.println("");

    serializeJson(json_request, buffer, sizeof(buffer));

    HTTPClient http;
    http.begin(host);
    http.addHeader("Content-Type", "application/json");
    int status_code = http.POST((uint8_t *)buffer, strlen(buffer));
    Serial.printf("status_code=%d\r\n", status_code);
    if (status_code == 200)
    {
        Stream *resp = http.getStreamPtr();

        DynamicJsonDocument json_response(255);
        deserializeJson(json_response, *resp);

        serializeJson(json_response, Serial);
        Serial.println("");
    }
    http.end();

    delay(5000);
}
