pyqt 설치방법

window - cmd - pip install pyqt5

raspberry - sudo apt-get install python3-pyqt5

실행해야하는 파일은 main.py

IPC 방식 Queue방식에서 공유메모리 사용으로 변경, List 자료구조 사용

프로세스 실행 시 기본 설정값들을 default.txt 파일에서 읽어들이고 공유메모리에 저장프

default.txt파일은 한 줄씩 now_temp, target_temp, beer_percent, amount_per_sec_mac, amount_per_sec_sso, servo 순으로 저장되어 있음

UI 종료시 3번까지 다시 실행

UI 디자인 변화

메인

![ui_main](https://user-images.githubusercontent.com/81142510/121224264-5975c380-c8c3-11eb-8903-53cbe27d9143.PNG)

![UI_home](https://user-images.githubusercontent.com/81142510/121224290-5f6ba480-c8c3-11eb-8b4c-f584a7447ac3.PNG)

![ui_monitor](https://user-images.githubusercontent.com/81142510/121224330-67c3df80-c8c3-11eb-8024-f3cf7368ba1b.PNG)

![ui_parameter](https://user-images.githubusercontent.com/81142510/121224341-6b576680-c8c3-11eb-8e31-40d2bc41e043.PNG)

![ui_setting](https://user-images.githubusercontent.com/81142510/121224354-6db9c080-c8c3-11eb-8e46-b3bb5699a199.PNG)

setting 화면은 제작예정 - 기본값 설정 및 부저음 설정기능 추가예정
