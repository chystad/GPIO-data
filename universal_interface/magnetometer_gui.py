import tkinter as tk
import numpy as np
import math
import threading
import serial
import time
import re
import datetime

# Communication variables
port = '/dev/ttyUSB0'
baud_rate = 9600
# baud_rate = 19200

# Other variables
maxAzim = 9999
maxElev = 2500
maxBank = 5000
transformed_horizon_mark_vec = np.array([
    [0],
    [0]
])


def lintrans(vec, theta):
    # returns a 2x1 vector that is rotated theta degrees with respect to vec 
    # Rotation matrix for a rotation in the xy-plane
    R = np.array([
        [math.cos(theta),  -math.sin(theta)],
        [math.sin(theta),   math.sin(theta)]
    ])
    retval = R @ vec
    return retval


def map_angle(angle, maxInputAngle, maxOutputAngle):
    # returns an angle with a given max value, i.e. maps the input range [0, 9999] to [0, 360], or [-2500, 2500] to [-90, 90]
    mappedAngle = angle / maxInputAngle * maxOutputAngle
    return round(mappedAngle, 2)


def write_to_file(telemetry):
    # log serial data to .txt file
    now = datetime.datetime.now()
    timestamp = now.strftime("%d-%m-%Y %H:%M:%S") + "." + now.strftime("%f")[:3]
    log_entry = f"{timestamp}: {telemetry}\n"
    with open("serial_log.txt", "a") as log_file:
        log_file.write(log_entry)  # Write to file
        log_file.flush()  # Ensure it's written to disk immediately


def draw_compass(canvas, azimuth, elevation, bank):
    canvas.delete("all")
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    center_x, center_y = width // 2, height // 2
    radius = min(center_x, center_y) - 40
    horizon_width = 2*radius - radius*0.5
    horizon_blank_width = radius*0.3
    horizon_mark_width = radius*0.1
    vertical_horizon_scaling = 2.3

    # Compass circle
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="black")

    # Azimuth arrow
    azimuth_rad = math.radians(azimuth - 90)
    end_x = center_x + radius * math.cos(azimuth_rad)
    end_y = center_y + radius * math.sin(azimuth_rad)
    canvas.create_line(center_x, center_y, end_x, end_y, arrow=tk.LAST, fill="red", width=3)

    # Left horizon indicator (elevation and bank dependent)
    horizon_center_y = center_y + elevation*vertical_horizon_scaling
    bank_rad = math.radians(bank)
    horizon_start_x = center_x - horizon_width/2*math.cos(bank_rad)
    horizon_start_y = horizon_center_y - horizon_width/2*math.sin(bank_rad)
    horizon_end_x = center_x - horizon_blank_width/2*math.cos(bank_rad)
    horizon_end_y = horizon_center_y - horizon_blank_width/2*math.sin(bank_rad)
    canvas.create_line(horizon_start_x, horizon_start_y, horizon_end_x, horizon_end_y, fill="black", width=3)

    horizon_mark_vec = np.array([
        [horizon_mark_width],
        [0]
    ])
    transformed_horizon_mark_vec = lintrans(horizon_mark_vec, bank_rad+np.pi/2)
    horizon_mark_end_x = horizon_end_x + int(transformed_horizon_mark_vec[0][0])
    horizon_mark_end_y = horizon_end_y + int(transformed_horizon_mark_vec[1][0])
    canvas.create_line(horizon_end_x, horizon_end_y, horizon_mark_end_x, horizon_mark_end_y, fill="black", width=3)

    # Rifht horizon indicator (elevation and bank dependent)
    horizon_center_y = center_y + elevation*vertical_horizon_scaling
    bank_rad = math.radians(bank)
    horizon_start_x = center_x + horizon_width/2*math.cos(bank_rad)
    horizon_start_y = horizon_center_y + horizon_width/2*math.sin(bank_rad)
    horizon_end_x = center_x + horizon_blank_width/2*math.cos(bank_rad)
    horizon_end_y = horizon_center_y + horizon_blank_width/2*math.sin(bank_rad)
    canvas.create_line(horizon_start_x, horizon_start_y, horizon_end_x, horizon_end_y, fill="black", width=3)

    horizon_mark_end_x = horizon_end_x + int(transformed_horizon_mark_vec[0][0])
    horizon_mark_end_y = horizon_end_y + int(transformed_horizon_mark_vec[1][0])
    canvas.create_line(horizon_end_x, horizon_end_y, horizon_mark_end_x, horizon_mark_end_y, fill="black", width=3)

    # Center dot (NB! No scaling...)
    canvas.create_line(center_x-2, horizon_center_y, center_x+2, horizon_center_y, fill="black", width=4)

    # Azimuth, elevation and bank text
    canvas.create_text(width - 100, height - 42, text="Azimuth:")
    canvas.create_text(width - 35, height - 42, text=f"{azimuth}°")
    canvas.create_text(width - 105, height - 28, text="Elevation:")
    canvas.create_text(width - 35, height - 28, text=f"{elevation}°")
    canvas.create_text(width - 91, height - 14, text="Bank:")
    canvas.create_text(width - 35, height - 14, text=f"{bank}°")
    
    himmelretning_text = ['N', 'Ø', 'S', 'V']
    canvas.create_text(center_x, center_y - radius - 10, text=himmelretning_text[0], font=("Helvetica", 20, "bold"))
    canvas.create_text(center_x + radius + 14, center_y + 3, text=himmelretning_text[1], font=("Helvetica", 20, "bold"))
    canvas.create_text(center_x, center_y + radius + 20, text=himmelretning_text[2], font=("Helvetica", 20, "bold"))
    canvas.create_text(center_x - radius - 12, center_y + 3, text=himmelretning_text[3], font=("Helvetica", 20, "bold"))
    

def hør_etter_asimut_over_UART(canvas, port):
    print(f"Listening for updates on port {port}...")
    azimuth = 0
    elevation = 0
    bank = 0
    try:
        # Setup serial communication
        ser = serial.Serial(port, baud_rate, timeout=1)
        print(f"Opened serial communication on {port} with {baud_rate} baud rate.")
        
        # Continously read and print lines received over serial 
        while True:
            if ser.in_waiting > 0:
                #line = ser.readline().decode('utf-8').rstrip()
                line = ser.read(ser.in_waiting).decode('utf-8').rstrip()
                print(line)

                # If-sentence to ensure the string received over serial is formatted correctly.
                # This is a super monkey-brain way to solve this problem, as it just disregards the whole line
                # completely even if there is some useful information present in the string. 
                if(len(line) >= 20):
                    write_to_file(line)

                    # Use regular expression to find numbers with optional preceding signs
                    parts = re.findall(r'([+-]?\s*\d+)', line)

                    # If-sentence to check if three values are present in the string (azim, elev and bank)
                    if(len(parts) == 3):

                        # Process matches to extract azimuth, elevation angle, and bank angle
                        # Strip spaces and convert to integers, applying the sign correctly
                        cleaned_part_azim = parts[0].replace(" ", "")
                        cleaned_part_elev = parts[1].replace(" ", "")
                        cleaned_part_bank = parts[2].replace(" ", "")


                        try:
                            azimuth = int(cleaned_part_azim) 
                            elevation = int(cleaned_part_elev) 
                            bank = int(cleaned_part_bank)  
                            
                            lastTrueAzimuth = azimuth
                            lastTrueElevation = elevation
                            lastTrueBank = bank
                            
                            
                        except ValueError as e:
                            print(f"Error converting to integer: {e}")
                            azimuth = lastTrueAzimuth
                            elevation = lastTrueElevation
                            bank = lastTrueBank
                    


                    # Only received azimuth and elevation
                    elif(len(parts)==2): 
                        # Process matches to extract azimuth, elevation angle, and bank angle
                        # Strip spaces and convert to integers, applying the sign correctly
                        cleaned_part_azim = parts[0].replace(" ", "")
                        cleaned_part_elev = parts[1].replace(" ", "")


                        try:
                            azimuth = int(cleaned_part_azim)
                            elevation = int(cleaned_part_elev)
                            
                            lastTrueAzimuth = azimuth
                            lastTrueElevation = elevation
                            
                            
                        except ValueError as e:
                            print(f"Error converting to integer: {e}")
                            azimuth = lastTrueAzimuth
                            elevation = lastTrueElevation
                            bank = lastTrueBank

                #print(f"azim: {azimuth}, elev: {elevation}, bank: {bank}")
                azimuth_360 = map_angle(azimuth, maxAzim, 360)
                elevation_pm90 = -1 * map_angle(elevation, maxElev, 90)
                bank_pm180 = -1 * map_angle(bank, maxBank, 180)
                
                canvas.after(0, draw_compass, canvas, azimuth_360, elevation_pm90, bank_pm180)
            time.sleep(0.1)  # Liten pause for å ikke spamme ned systemet 

    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")

    except KeyboardInterrupt:
        print("Exiting...")

    finally:
        if 'ser' in locals() or 'ser' in globals():
            ser.close()
            print("Serial communication closed")



# Set up tkinter GUI
root = tk.Tk()
root.title("Compass UI")
root.geometry("500x500")

compass_canvas = tk.Canvas(root, width=400, height=400, bg="white")
compass_canvas.pack(fill="both", expand=True)

# Start UART kommunikasjon
threading.Thread(target=hør_etter_asimut_over_UART, args=(compass_canvas, port,), daemon=True).start()

root.mainloop()
