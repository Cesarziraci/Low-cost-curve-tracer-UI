import serial
from utils.constants import port, baudrate
from UI.dialogs import CustomDialog

try:
    ser = serial.Serial(port = port, baudrate= baudrate)
except Exception:
    dialog = CustomDialog('ERROR', 'COM port not found', [])
    dialog.open()

def write(message):
    ser.write(message)

def get(outData_x, outData_y, beta):
    while True:

        data = ser.readline().decode('utf-8').strip()

        if data.startswith('X=') and ', Y=' and '' in data:

            x_index = data.find('X=') + 2
            y_index = data.find(', Y=') + 4

            x_value = float(data[x_index:y_index - 4])
            y_value = float(data[y_index:])

            outData_x.append(x_value)
            outData_y.append(y_value)