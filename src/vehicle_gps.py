import serial

ser = serial.Serial(
    port="/dev/ttyS0",
    baudrate=38400
)

while True:
    print(ser.readline().hex())