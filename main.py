from fastapi import FastAPI, HTTPException
import RPi.GPIO as GPIO
import time

app = FastAPI(title="Raspberry Pi Zero Motor Control API")

# GPIO 설정
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# ESC 제어를 위한 PWM 설정
ESC_PIN = 18  # ESC가 연결된 GPIO 핀
ESC_FREQ = 50  # 50Hz PWM 주파수
ESC_MIN_DUTY = 5  # 최소 듀티 사이클 (%)
ESC_MAX_DUTY = 10  # 최대 듀티 사이클 (%)

# 서보 모터 제어를 위한 PWM 설정
SERVO_PIN = 17  # 서보 모터가 연결된 GPIO 핀
SERVO_FREQ = 50  # 50Hz PWM 주파수
SERVO_MIN_DUTY = 2.5  # 최소 듀티 사이클 (%)
SERVO_MAX_DUTY = 12.5  # 최대 듀티 사이클 (%)

# PWM 객체 초기화
esc_pwm = GPIO.PWM(ESC_PIN, ESC_FREQ)
servo_pwm = GPIO.PWM(SERVO_PIN, SERVO_FREQ)

# PWM 시작
esc_pwm.start(0)
servo_pwm.start(0)

@app.on_event("startup")
async def startup_event():
    # ESC 초기화
    esc_pwm.ChangeDutyCycle(ESC_MIN_DUTY)
    time.sleep(2)  # ESC 초기화 대기

@app.on_event("shutdown")
async def shutdown_event():
    # 모든 PWM 정지 및 GPIO 정리
    esc_pwm.stop()
    servo_pwm.stop()
    GPIO.cleanup()

@app.get("/")
async def root():
    return {"message": "Raspberry Pi Zero Motor Control API"}

@app.post("/esc/speed/{speed}")
async def set_esc_speed(speed: int):
    if not 0 <= speed <= 100:
        raise HTTPException(status_code=400, detail="Speed must be between 0 and 100")
    
    # 속도를 듀티 사이클로 변환
    duty_cycle = ESC_MIN_DUTY + (ESC_MAX_DUTY - ESC_MIN_DUTY) * (speed / 100)
    esc_pwm.ChangeDutyCycle(duty_cycle)
    return {"message": f"ESC speed set to {speed}%"}

@app.post("/servo/angle/{angle}")
async def set_servo_angle(angle: int):
    if not 0 <= angle <= 180:
        raise HTTPException(status_code=400, detail="Angle must be between 0 and 180")
    
    # 각도를 듀티 사이클로 변환
    duty_cycle = SERVO_MIN_DUTY + (SERVO_MAX_DUTY - SERVO_MIN_DUTY) * (angle / 180)
    servo_pwm.ChangeDutyCycle(duty_cycle)
    return {"message": f"Servo angle set to {angle}°"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 