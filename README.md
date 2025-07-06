# Raspberry Pi Zero Motor Control API

라즈베리파이 제로에서 ESC와 서보 모터를 제어하는 Python FastAPI 서버입니다.

## 하드웨어 연결

- PCA9685 PWM 컨트롤러를 I2C로 연결
- ESC: 채널 0번에 연결
- 서보 모터: 채널 1번에 연결

## 설치 방법

1. I2C 활성화:
```bash
# I2C 활성화
sudo raspi-config
# Interface Options > I2C > Enable
```

2. Python 가상 환경 설정:
```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
source venv/bin/activate  # Linux/Mac
# 또는
.\venv\Scripts\activate  # Windows
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