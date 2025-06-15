# Raspberry Pi Zero ESC Control API

라즈베리파이 제로에서 ESC를 제어하는 Go 웹 서버입니다.

## 하드웨어 연결

- ESC: GPIO 18번 핀에 연결

## 설치 방법

1. GPIO 권한 설정:
```bash
# gpio 그룹에 현재 유저 추가
sudo usermod -a -G gpio $USER

# 변경사항을 적용하기 위해 재로그인하거나 다음 명령어 실행
newgrp gpio
```

2. Go 설치 (1.16 이상):
```bash
# 라즈베리파이에서 Go 설치
wget https://golang.org/dl/go1.21.6.linux-armv6l.tar.gz
sudo tar -C /usr/local -xzf go1.21.6.linux-armv6l.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

3. 의존성 설치:
```bash
go mod download
```

4. 서버 실행:
```bash
go run main.go
```

5. 바이너리 빌드 (선택사항):
```bash
go build -o esc-control
./esc-control
```

## API 엔드포인트

### ESC 제어
- `POST /esc/speed/{speed}`
  - speed: 0-100 사이의 정수값 (속도 %)

## 사용 예시

ESC 속도 설정:
```bash
curl -X POST "http://localhost:8000/esc/speed/50"
```

## 주의사항

1. GPIO 접근 권한이 없는 경우 "Permission denied" 오류가 발생할 수 있습니다.
2. 권한 설정 후에도 문제가 지속되면 라즈베리파이를 재부팅해보세요.
3. 서버 실행 시 sudo 권한이 필요하지 않도록 반드시 GPIO 권한 설정을 먼저 진행해주세요.
4. ESC 초기화를 위해 서버 시작 시 최소 신호(5% 듀티 사이클)를 2초간 전송합니다.