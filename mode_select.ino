#include "arduinoFFT.h"

#define BTN_PIN         13 
#define LED_GREEN       12  
#define LED_RED         14  
#define ADC_PIN         36  
#define DAC_PIN         25  

#define SAMPLES         512   
#define SAMPLING_FREQ   10000 
#define ALARM_THRESHOLD 20000 

double vReal[SAMPLES];
double vImag[SAMPLES];
ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, SAMPLES, SAMPLING_FREQ);

volatile bool modeChanged = false;
int currentMode = 0; 

unsigned long lastDebounceTime = 0;
unsigned int sampling_period_us;

void IRAM_ATTR handleButtonPress() {
  if ((millis() - lastDebounceTime) > 200) {
    currentMode = !currentMode; 
    modeChanged = true;
    lastDebounceTime = millis();
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(BTN_PIN, INPUT_PULLDOWN); 
  attachInterrupt(digitalPinToInterrupt(BTN_PIN), handleButtonPress, RISING);
  
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);

  sampling_period_us = round(1000000 * (1.0 / SAMPLING_FREQ));
}

void loop() {
  
  digitalWrite(LED_GREEN, HIGH);

  for (int k=0; k<100; k++) {
      float t = millis()/1000.0;
      float val = 127 + 120 * sin(2 * PI * 50 * t); 
      dacWrite(DAC_PIN, (int)val);
      delayMicroseconds(100); 
  }

  for(int i=0; i<SAMPLES; i++) {
    unsigned long mic = micros();
    
    vReal[i] = analogRead(ADC_PIN); 
    vImag[i] = 0;

    float val = 127 + 120 * sin(2 * PI * 50 * (millis()/1000.0));
    dacWrite(DAC_PIN, (int)val);
    
    while(micros() < (mic + sampling_period_us)) { }
  }
  
  digitalWrite(LED_GREEN, LOW);
  
  if (currentMode == 0) {
    FFT.windowing(FFT_WIN_TYP_HAMMING, FFT_FORWARD);
    FFT.compute(FFT_FORWARD);
    FFT.complexToMagnitude();
    double peak = FFT.majorPeak();

    if (peak > 5) {
        if(peak > 45 && peak < 55) digitalWrite(LED_RED, HIGH);
        else digitalWrite(LED_RED, LOW);
    }

    Serial.print("MODE:FFT,Peak:");
    Serial.print(peak);
    Serial.print(",Data:");
    for(int i=2; i<60; i++) {
        Serial.print(vReal[i]);
        if(i<59) Serial.print(",");
    }
    Serial.println();
    
  } else {
    digitalWrite(LED_RED, LOW);

    Serial.print("MODE:RAW,Peak:0,Data:");
    for(int i=0; i<100; i++) { 
        Serial.print(vReal[i]);
        if(i<99) Serial.print(",");
    }
    Serial.println();
  }
}