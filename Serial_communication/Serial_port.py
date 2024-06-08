import serial
from utils.constants import Data, port, baudrate

ser = serial.Serial(port = port, baudrate= baudrate)

def get(outData_x, outData_y):
    while True:

        data = ser.readline().decode().strip()

        if data.startswith('X=') and ', Y=' in data:

            x_index = data.find('X=') + 2
            y_index = data.find(', Y=') + 4

            x_value = float(data[x_index:y_index - 4])
            y_value = float(data[y_index:])

            Data.Voltage.append(x_value)
            Data.Current.append(y_value)