import serial

# 먼저 9600
try:
    ser = serial.Serial("/dev/ttyTHS1", 9600, timeout=1)
    print("9600bps 시도")
    for i in range(10):
        print(ser.readline().decode(errors="ignore").strip())
except:
    print("9600 실패")

# 다음 38400
try:
    ser = serial.Serial("/dev/ttyTHS1", 38400, timeout=1)
    print("38400bps 시도")
    for i in range(10):
        print(ser.readline().decode(errors="ignore").strip())
except:
    print("38400 실패")
