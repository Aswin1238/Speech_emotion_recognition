#include <Speech_Emotion_Recognition_inferencing.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Microphone settings
#define MIC_PIN 34
#define SAMPLE_RATE 16000
static int16_t audio_buffer[EI_CLASSIFIER_RAW_SAMPLE_COUNT];

// Callback to feed audio to Edge Impulse
int microphone_audio_signal_get_data(size_t offset, size_t length, float *out_ptr) {
  for (size_t i = 0; i < length; i++) {
    out_ptr[i] = (float)audio_buffer[offset + i] / 32768.0f;
  }
  return 0;
}

void setup() {
  Serial.begin(115200);
  delay(1000);

  // OLED setup
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println("OLED init failed!");
    while (1);
  }
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(10, 25);
  display.println("Speech Emotion AI");
  display.display();
  delay(1500);

  // Microphone setup
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  Serial.println("🎙 Ready to detect emotion...");
}

void loop() {
  // Record 1 second of audio
  for (int i = 0; i < EI_CLASSIFIER_RAW_SAMPLE_COUNT; i++) {
    int adc = analogRead(MIC_PIN) - 2048;
    audio_buffer[i] = adc << 4;
    delayMicroseconds(1000000 / SAMPLE_RATE);
  }

  // Run classifier
  ei::signal_t signal;
  signal.total_length = EI_CLASSIFIER_RAW_SAMPLE_COUNT;
  signal.get_data = &microphone_audio_signal_get_data;

  ei_impulse_result_t result = {0};
  EI_IMPULSE_ERROR err = run_classifier(&signal, &result, false);
  if (err != EI_IMPULSE_OK) {
    Serial.printf("Classifier error: %d\n", err);
    return;
  }
}
