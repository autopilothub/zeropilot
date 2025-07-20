from fastapi import FastAPI, Query
from smbus2 import SMBus
import time

app = FastAPI()
bus = SMBus(8)
I2C_ADDR = 0x40
ESC_CH = 0
SERVO_CH = 1

current_angle = 100  # 초기 각도

def pwm_init():
    bus.write_byte_data(I2C_ADDR, 0x00, 0x10)
    bus.write_byte_data(I2C_ADDR, 0xFE, 121)
    bus.write_byte_data(I2C_ADDR, 0x00, 0x00)
    time.sleep(0.005)
    bus.write_byte_data(I2C_ADDR, 0x00, 0xA1)

def set_pwm(channel, on, off):
    base = 0x06 + 4 * channel
    bus.write_byte_data(I2C_ADDR, base, on & 0xFF)
    bus.write_byte_data(I2C_ADDR, base + 1, on >> 8)
    bus.write_byte_data(I2C_ADDR, base + 2, off & 0xFF)
    bus.write_byte_data(I2C_ADDR, base + 3, off >> 8)

def set_pwm_us(channel, pulse_us):
    ticks = int(pulse_us * 4096 / 20000)
    set_pwm(channel, 0, ticks)

def set_servo_angle(channel, angle):
    pulse = 500 + (angle / 180.0) * 1900
    set_pwm_us(channel, pulse)

@app.on_event("startup")
def on_start():
    global current_angle
    pwm_init()
    set_servo_angle(SERVO_CH, current_angle)

# ✅ ESC 제어 (GET 방식)
@app.get("/esc")
def get_esc(speed: int = Query(..., ge=-70, le=70)):
    NEUTRAL_US = 1640
    PWM_RANGE = 400
    pulse = NEUTRAL_US + (speed / 100.0) * PWM_RANGE
    set_pwm_us(ESC_CH, pulse)
    return {"ESC": f"Set to {speed}%"}

# ✅ 서보 제어 (GET 방식)
@app.get("/servo")
def get_servo(angle: int = Query(...)):
    global current_angle
    if 60 <= angle <= 140:
        current_angle = angle
        set_servo_angle(SERVO_CH, angle)
        return {"Servo": f"✅ Set to {angle}°"}
    else:
        return {"Servo": f"⚠️ Out of range: Kept at {current_angle}°"}

