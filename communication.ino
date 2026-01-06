#include "arduinoFFT.h"

#define SAMPLES         512             
#define SAMPLING_FREQ   10000           
#define ADC_PIN         36              
#define DAC_PIN         25              
#define DEBUG_PIN       4               

unsigned int sampling_period_us;
unsigned long microseconds;

double vReal[SAMPLES];
double vImag[SAMPLES];

ArduinoFFT<double> FFT = ArduinoFFT<double>(vReal, vImag, SAMPLES, SAMPLING_FREQ);

void setup() {
  Serial.begin(115200);           
  pinMode(DEBUG_PIN, OUTPUT);     
  digitalWrite(DEBUG_PIN, LOW);
  
  sampling_period_us = round(1000000 * (1.0 / SAMPLING_FREQ));
  
  Serial.println("System Ready: Signal Generator & FFT Analyzer");
}

void loop() {
  static float t = 0;
  float val = 127 + 120 * sin(2 * PI * 50 * t);
  dacWrite(DAC_PIN, (int)val);
  t += 0.001; 

  for(int i=0; i<SAMPLES; i++) {
    microseconds = micros();   
    
    vReal[i] = analogRead(ADC_PIN); 
    vImag[i] = 0;                   
    
    val = 127 + 120 * sin(2 * PI * 50 * (millis()/1000.0));
    dacWrite(DAC_PIN, (int)val);

    while(micros() < (microseconds + sampling_period_us)){
    }
  }
  digitalWrite(DEBUG_PIN, HIGH); 
  FFT.windowing(FFT_WIN_TYP_HAMMING, FFT_FORWARD);
  FFT.compute(FFT_FORWARD);
  FFT.complexToMagnitude();
  double peak = FFT.majorPeak();
  digitalWrite(DEBUG_PIN, LOW); 
  Serial.print("Peak:");
  Serial.println(peak, 2);
  Serial.print("Data:");
  for(int i=2; i<60; i++) { 
      Serial.print(vReal[i]);
      if(i < 59) Serial.print(",");
  }
  Serial.println();

  delay(100);
}