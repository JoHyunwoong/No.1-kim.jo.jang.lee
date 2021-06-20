**pyqt 설치방법**

<window>
cmd - pip install pyqt5(환경변수 설정해주어야 함)

<raspberry>
$ sudo apt-get install python3-pyqt5
  
  
**실행 방법**
  1. 라즈베리파이 부팅
  2. setting.sh 실행
  3. main.py 실행


IPC 방식 : Queue방식에서 공유메모리 사용으로 변경, List 자료구조 사용

프로세스 실행 시 기본 설정값들을 default.txt 파일에서 읽어들이고 공유메모리에 저장

default.txt파일은 한 줄씩 now_temp, target_temp, beer_percent, amount_per_sec_mac, amount_per_sec_sso 순으로 저장되어 있음

UI 종료시 3번까지 다시 실행

UI 디자인 변화

**UI 실행 화면**

![ui_main](https://user-images.githubusercontent.com/81142510/121224264-5975c380-c8c3-11eb-8903-53cbe27d9143.PNG)

![UI_home2](https://user-images.githubusercontent.com/81142510/121378428-28a69480-c97e-11eb-9fc3-6ff26b25649f.PNG)

![ui_monitor2](https://user-images.githubusercontent.com/81142510/121378548-4116af00-c97e-11eb-8e78-3c943aeec30f.PNG)

![ui_parameter](https://user-images.githubusercontent.com/81142510/121224341-6b576680-c8c3-11eb-8e31-40d2bc41e043.PNG)

![ui_setting](https://user-images.githubusercontent.com/81142510/122669894-484d8080-d1fa-11eb-8941-fe42eb34103d.PNG)


setting 화면은 제작예정

기본값 설정 및 부저음 설정기능 추가예정
