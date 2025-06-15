# Raspberry Pi Zero Motor Control API

라즈베리파이 제로에서 ESC와 서보 모터를 제어하는 FastAPI 서버입니다.

## 하드웨어 연결

- ESC: GPIO 18번 핀에 연결
- 서보 모터: GPIO 17번 핀에 연결

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 서버 실행:
```bash
python main.py
```

## API 엔드포인트

### ESC 제어
- `POST /esc/speed/{speed}`
  - speed: 0-100 사이의 정수값 (속도 %)

### 서보 모터 제어
- `POST /servo/angle/{angle}`
  - angle: 0-180 사이의 정수값 (각도)

## 사용 예시

ESC 속도 설정:
```bash
curl -X POST "http://localhost:8000/esc/speed/50"
```

서보 모터 각도 설정:
```bash
curl -X POST "http://localhost:8000/servo/angle/90"
```