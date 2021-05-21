from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import QPropertyAnimation, QThread, pyqtSignal
from ui_version2 import Ui_MainWindow
import sys
from queue import Queue
from threading import Thread
from pump import *

class MainWindow(QMainWindow):
    def __init__(self, q):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.q = q
        self.consumer = Consumer(self.q)
        self.consumer.poped.connect(self.show_popup)
        self.consumer.start()
        self.first_percent = 30         # 초기값 설정
        self.second_percent = 70
        self.amount_sso = 360
        self.amount_mac = 500
        self.ui.display_first_percent.display(str(self.first_percent))
        self.ui.display_second_percent.display(str(self.second_percent))
        self.ui.display_remains1.display(str(self.amount_sso))
        self.ui.display_remains2.display(str(self.amount_mac))
        self.ui.Pages_Widget.setCurrentWidget(self.ui.home_page)

        self.ui.Btn_Toggle.clicked.connect(lambda: self.toggleMenu(200, True))
        self.ui.home_btn.clicked.connect(self.showhomepage)
        self.ui.monitor_btn.clicked.connect(self.showmonitor)
        self.ui.setting_btn.clicked.connect(self.showsetting)

        self.ui.up1_btn.clicked.connect(self.up1)
        self.ui.up2_btn.clicked.connect(self.up2)
        self.ui.start_btn.clicked.connect(self.makestart)

        self.ui.replace_btn1.clicked.connect(self.replace_sso)
        self.ui.replace_btn2.clicked.connect(self.replace_mac)
        self.show()

    # 페이지 기능
    def showhomepage(self):
        self.ui.Pages_Widget.setCurrentWidget(self.ui.home_page)

    def showmonitor(self):
        self.ui.Pages_Widget.setCurrentWidget(self.ui.monitor_page)

    def showsetting(self):
        self.ui.Pages_Widget.setCurrentWidget(self.ui.setting_page)

    # 농도 업다운 기능
    def up1(self):
        if self.first_percent != 100:
            self.first_percent += 10
            self.second_percent -= 10
        self.ui.display_first_percent.display(str(self.first_percent))
        self.ui.display_second_percent.display(str(self.second_percent))

    def up2(self):
        if self.second_percent != 100:
            self.first_percent -= 10
            self.second_percent += 10
        self.ui.display_first_percent.display(str(self.first_percent))
        self.ui.display_second_percent.display(str(self.second_percent))

    # 스타트기능
    def makestart(self):        # 제조시작
        self.ui.start_btn.setEnabled(False)     # 중복실행을 위해 버튼 비활성화
        p1 = Thread(target=self.worker, args=(self.q,))
        p1.start()


    # ui기능
    def toggleMenu(self, maxWidth, enable):         # 토글기능구현
        if enable:

            width = self.ui.frame_leftmenu.width()
            maxExtend = maxWidth
            standard = 70

            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.frame_leftmenu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.start()

    # 오류 팝업
    def show_popup(self, data):
        if data == str(1):
            msg = QMessageBox()         # pump error
            msg.setWindowTitle("오류 발생")
            msg.setText("펌프에서 문제가 발생했습니다.")
            x = msg.exec_()
        elif data == str(2):            # shortage
            msg = QMessageBox()
            msg.setWindowTitle("음료 부족")
            msg.setText("음료가 부족합니다.")
            x = msg.exec_()
        elif data == str(0):
            self.ui.display_remains1.display(str(self.amount_sso))
            self.ui.display_remains2.display(str(self.amount_mac))
        self.ui.start_btn.setEnabled(True)

    # 음료 리필
    def replace_sso(self):
        self.amount_sso = 360
        self.ui.display_remains1.display(str(self.amount_sso))

    def replace_mac(self):
        self.amount_mac = 500
        self.ui.display_remains2.display(str(self.amount_mac))

    # pump worker
    def worker(self, q):
        pump_error_value, self.amount_sso, self.amount_mac = pumpAlcohol(self.first_percent/100, self.amount_sso, self.amount_mac)
        print(pump_error_value, self.amount_sso, self.amount_mac) # test print
        q.put(str(pump_error_value))
        #if pump_error_value == 0:
            #buzzer()

# speaker process
#def buzzer():
    # buzzer

# read q and connect thread
class Consumer(QThread):
    poped = pyqtSignal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.poped.emit(data)

def main():
    q = Queue()
    app = QApplication(sys.argv)
    main_win = MainWindow(q)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
'''
if __name__ == '__main__':
    q = Queue()

    app = QApplication(sys.argv)
    main_win = MainWindow(q)
    sys.exit(app.exec_())
    '''
