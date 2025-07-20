from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'  # 실제 연결된 포트에 따라 변경

lidar = RPLidar(PORT_NAME)
lidar.start_motor()
info =lidar.get_info()
print(info)

try:
    print("Start scanning...")
    for scan in lidar.iter_scans():
        for (_, angle, distance) in scan:
            # angle: 0~360도, distance: mm
            if (angle >= 350 or angle <= 10):  # 정면 방향 (0도 ± 10도)
                if distance > 0 and distance < 1000:  # 1m 이내에 물체
                    print(f"[!] 전방에 물체 감지: 거리 {distance:.1f}mm, 각도 {angle:.1f}")
except KeyboardInterrupt:
    print("Stopping.")
finally:
    lidar.stop()
    lidar.disconnect()
