#include <FastLED.h>

#define LED_PIN     5
#define NUM_LEDS    12
#define BRIGHTNESS  50
#define LED_TYPE    WS2811
#define COLOR_ORDER GRB
CRGB leds[NUM_LEDS];


CRGBPalette16 currentPalette;
TBlendType    currentBlending;

char msg[5];


void setLed(int i, int paletteIdx, int brightness) {
  leds[i] = ColorFromPalette(currentPalette, paletteIdx, brightness, currentBlending);
}


void setup() {
    delay( 3000 ); // power-up safety delay
    Serial.begin(9600);
    FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
    FastLED.setBrightness(BRIGHTNESS);
    
    currentPalette = RainbowColors_p;
    currentBlending = LINEARBLEND;
    
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = ColorFromPalette(currentPalette, 0, 0, currentBlending);
    };
}


void loop() {
    FastLED.show();

    if (Serial.available() > 0) {
      Serial.readBytes(msg, 5);
      if (msg[0] != '?' || msg[4] != '!') {
        Serial.println("ojej, fakap!");
      } else {
        setLed(msg[1], msg[2], msg[3]);
        Serial.println(msg);
      }
    }
}

