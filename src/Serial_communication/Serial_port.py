import serial
from utils.constants import Data, baudrate, port

ser = serial.Serial(port=port, baudrate=baudrate)

def write(message):
    ser.write(message.encode())

def get():
    while True:
        data = ser.readline().decode('ascii').strip()
        if data.startswith('X= ') and ',Y= ' in data or ' ,B= ' in data:
            print(data)
            x_index = data.find('X= ') + 3
            y_index = data.find(',Y= ') + 4
            b_index = data.find(',B= ') + 4

            x_value = float(data[x_index:x_index + 4]) 
            y_value = float(data[y_index:y_index + 5])
            b_value = float(data[b_index:b_index + 6])

            Data.Voltage.append(x_value)
            Data.Current.append(y_value)
            Data.beta = b_value