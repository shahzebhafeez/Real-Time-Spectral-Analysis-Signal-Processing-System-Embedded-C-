import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import threading
import time

SERIAL_PORT = 'COM3'  
BAUD_RATE = 115200

data_lock = threading.Lock()
y_data = np.zeros(50)
x_data = np.arange(0, 50)
peak_freq = 0.0
current_mode = "FFT"

try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2) 
    print(f"Connected to {SERIAL_PORT}")
except Exception as e:
    print(f"Error: {e}")
    exit()

def read_serial():
    global y_data, peak_freq, current_mode
    while True:
        try:
            raw_line = ser.readline().decode('utf-8', errors='ignore').strip()
            
            if "MODE:FFT" in raw_line:
                current_mode = "FFT"
            elif "MODE:RAW" in raw_line:
                current_mode = "RAW"

            if "Peak:" in raw_line:
                parts = raw_line.split("Peak:")
                if len(parts) > 1:
                    val_str = parts[1].split(",")[0] 
                    try:
                        peak_freq = float(val_str)
                    except:
                        pass

            if "Data:" in raw_line:
                parts = raw_line.split("Data:")
                if len(parts) > 1:
                    data_str = parts[1]
                    new_data = np.fromstring(data_str, sep=',')
                    
                    if len(new_data) > 0:
                        with data_lock:
                            y_data = new_data
                            
        except Exception:
            pass

thread = threading.Thread(target=read_serial)
thread.daemon = True
thread.start()

fig, ax = plt.subplots()
line_plot, = ax.plot([], [], color='#00ff00') 

ax.set_facecolor('black')
fig.patch.set_facecolor('black')
ax.set_title("Real-Time Analysis Tool", color='white')
ax.tick_params(axis='x', colors='white')
ax.tick_params(axis='y', colors='white')

text_label = ax.text(0.5, 0.9, "Initializing...", transform=ax.transAxes, 
                     color='yellow', fontsize=14, ha='center')

def update(frame):
    global x_data
    
    with data_lock:
        current_y = y_data.copy()
    if len(x_data) != len(current_y):
        x_data = np.arange(len(current_y))
        line_plot.set_xdata(x_data)
        
        ax.set_xlim(0, len(current_y))
    
    line_plot.set_ydata(current_y)
    
    if current_mode == "FFT":
        text_label.set_text(f"FFT Mode | Peak: {peak_freq:.2f} Hz")
        text_label.set_color('yellow')
        ax.set_xlabel("Frequency Bin (Hz)", color='white')
        
        if np.max(current_y) > 100:
            ax.set_ylim(0, np.max(current_y) * 1.2)
            
    else:
        text_label.set_text("Oscilloscope Mode (Raw Signal)")
        text_label.set_color('cyan')
        ax.set_xlabel("Time (Samples)", color='white')
        
        ax.set_ylim(0, 4095) 

    return line_plot, text_label

ani = FuncAnimation(fig, update, interval=50, cache_frame_data=False)
plt.show()