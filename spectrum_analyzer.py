import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import time

SERIAL_PORT = 'COM3' 
BAUD_RATE = 115200

x_data = np.arange(0, 50)
y_data = np.zeros(50)
peak_freq = 0.0

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

def read_serial():
    global y_data, peak_freq, x_data
    while True:
        try:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            if "Peak:" in raw_line:
                parts = raw_line.split("Peak:")
                if len(parts) > 1:
                    peak_freq = float(parts[1])
            elif "Data:" in raw_line:
                parts = raw_line.split("Data:")
                if len(parts) > 1:
                    data_str = parts[1]
                    new_data = np.fromstring(data_str, sep=',')
                    
                    if len(new_data) > 0:
                        y_data = new_data
                        if len(x_data) != len(y_data):
                            x_data = np.arange(len(y_data))
                            line_plot.set_xdata(x_data)
                            
        except Exception as e:
            pass 

thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

fig, ax = plt.subplots()
line_plot, = ax.plot(x_data, y_data, color='#00ff00') 
ax.set_facecolor('black')
fig.patch.set_facecolor('black')

ax.set_title("Real-Time Vibration Spectrum (FFT)", color='white')
ax.set_xlabel("Frequency Bin", color='white')
ax.set_ylabel("Magnitude", color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')
text_label = ax.text(0.5, 0.9, "Waiting for Data...", transform=ax.transAxes, 
                     color='yellow', fontsize=14, ha='center')

def update(frame):
    line_plot.set_ydata(y_data)
    text_label.set_text(f"Peak Frequency: {peak_freq:.2f} Hz")
    current_max = np.max(y_data)
    if current_max > 100:
        ax.set_ylim(0, current_max * 1.1) 
        
    return line_plot, text_label

ani = FuncAnimation(fig, update, interval=50)
plt.show()