Real-Time Spectral Analysis & Industrial Protocol Diagnostic System
📌 Project Overview
An advanced embedded instrumentation tool built on the ESP32 to analyze vibration signals and simulate industrial protocols in real-time. The system utilizes onboard DSP (512-point FFT) to convert 10kHz analog signals into frequency spectra with <14ms latency, streaming data via UART to a multi-threaded Python/Matplotlib Dashboard. It features a "Protocol Simulator" engine for I2C/SPI physical layer debugging and a hardware-interrupt driven control interface.

🚀 Key Features
Real-Time DSP: Performs onboard FFT to detect vibration frequencies, visualizing data in both Spectrum Mode (Frequency) and Oscilloscope Mode (Time-Domain).

Embedded Control: Uses GPIO Interrupts (ISRs) for instant mode switching and implements a safety alarm that triggers if vibration energy exceeds thresholds.

Protocol Simulation: Generates active traffic for I2C (NACK testing) and SPI (0xDEADBEEF payload) to verify timing and bus arbitration using a Logic Analyzer.

Python Dashboard: A robust, multi-threaded GUI that handles high-speed serial data (115200 baud) with dynamic auto-scaling and error handling.

🛠 Tech Stack
Firmware: C++ (ESP32), arduinoFFT, Wire (I2C), SPI, FreeRTOS.

Software: Python 3.10, Matplotlib, PySerial, NumPy.

📊 Results
<14ms DSP processing time per frame (Verified via Logic Analyzer).

Successfully captured I2C NACK errors and SPI 0xDEADBEEF packets on physical lines.

Achieved <1% error in 50Hz fundamental frequency detection.

![Embedded_project](https://github.com/user-attachments/assets/8146e54c-4f28-45de-917e-00f4306a79ef)

https://github.com/user-attachments/assets/ed511292-e009-4b28-8a57-6a80bac361df

https://github.com/user-attachments/assets/c2928970-4e26-4502-a4e2-7e72e90f0ffe



