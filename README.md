# Jetson Xavier NX Motor Control API

Jetson Xavier NX에서 ESC와 서보 모터를 제어하는 Python FastAPI 서버입니다.

## 하드웨어 연결

### Jetson Xavier NX 핀 연결
- **I2C 연결**:
  - SDA: 핀 3 (GPIO2)
  - SCL: 핀 5 (GPIO3)
  - VCC: 3.3V
  - GND: GND

### PCA9685 PWM 컨트롤러 연결
- **I2C 주소**: 0x40 (기본값)
- **ESC**: 채널 0번에 연결
- **서보 모터**: 채널 1번에 연결

### 전원 공급
- **PCA9685 VCC**: 3.3V 또는 5V (서보 모터 전압에 따라)
- **PCA9685 GND**: GND
- **ESC 전원**: 별도 배터리 공급 권장
- **서보 모터 전원**: 5V 권장

## 설치 방법

1. I2C 활성화:
```bash
# I2C 활성화 (Jetson Xavier NX)
sudo apt-get update
sudo apt-get install i2c-tools
# I2C 버스 확인
i2cdetect -l
# I2C 디바이스 확인
i2cdetect -y 1
```

2. Python 가상 환경 설정:
```bash
# 가상 환경 생성
python3 -m venv venv

# 가상 환경 활성화
source venv/bin/activate
```

3. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

4. 서버 실행:
```bash
cd src
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API 엔드포인트

### ESC 제어
- `GET /esc?speed={speed}`
  - speed: -70에서 70 사이의 정수값 (속도 %)

### 서보 모터 제어
- `GET /servo?angle={angle}`
  - angle: 60에서 140 사이의 정수값 (각도)

## 사용 예시

ESC 속도 설정:
```bash
curl "http://localhost:8000/esc?speed=50"
```

서보 모터 각도 설정:
```bash
curl "http://localhost:8000/servo?angle=90"
```

## 주의사항

1. I2C가 활성화되어 있어야 합니다.
2. PCA9685 PWM 컨트롤러가 올바르게 연결되어 있어야 합니다.
3. 서보 모터는 60-140도 범위로 제한되어 있습니다.
4. ESC는 -70%에서 70% 범위로 제한되어 있습니다.
5. 가상 환경을 비활성화하려면 `deactivate` 명령어를 사용하세요.
6. Jetson Xavier NX는 ARM64 아키텍처이므로 호환되는 패키지를 설치해야 합니다.
7. ESC는 높은 전류를 사용하므로 별도 전원 공급을 권장합니다.
8. I2C 주소가 0x40이 아닌 경우 코드에서 수정이 필요합니다.