import serial
from utils.constants import Data,port, baudrate
from UI.dialogs import CustomDialog

ser = serial.Serial(port = port, baudrate= baudrate)

def write(message):
    ser.write(message.encode())

def get(dt):
    try:
        while True:
            data = ser.readline().decode('utf-8').strip()
            if data.startswith('X= ') and ',Y= ' in data and ',B= ' in data:

                x_index = data.find('X= ') + 3
                y_index = data.find(',Y= ') + 4
                b_index = data.find(',B= ') + 4

                x_value = float(data[x_index:x_index + 6]) 
                y_value = float(data[y_index:y_index + 6])
                b_value = float(data[b_index:b_index + 6])

                Data.Voltage.append(x_value)
                Data.Current.append(y_value)
                Data.beta = b_value
    except Exception:
        print('Serial Port Close')