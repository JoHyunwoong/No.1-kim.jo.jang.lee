from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import QPropertyAnimation, QThread, pyqtSignal
from ui_version1 import Ui_MainWindow
import sys
import time
from queue import Queue
from threading import Thread

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
        self.pump_error_value = 0
        self.ui.Pages_Widget.setCurrentWidget(self.ui.home_page)

        self.ui.Btn_Toggle.clicked.connect(lambda: self.toggleMenu(200, True))
        self.ui.home_btn.clicked.connect(self.showhomepage)
        self.ui.monitor_btn.clicked.connect(self.showmonitor)
        self.ui.setting_btn.clicked.connect(self.showsetting)

        self.ui.up1_btn.clicked.connect(self.up1)
        self.ui.up2_btn.clicked.connect(self.up2)
        self.ui.start_btn.clicked.connect(self.makestart)

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
        p1 = Thread(target=pump_worker, args=(self.q,))
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

    def show_popup(self, data):
        if data == str(2):
            msg = QMessageBox()         # pump error
            x = msg.exec_()
        elif data == str(1):            # shortage
            msg = QMessageBox()
            x = msg.exec_()
        elif data == str(0):
            p2 = Process(name="speaker", target=speaker_worker)
            p2.start()
        self.ui.start_btn.setEnabled(True)

# pump process
def pump_worker(q):
    data = str(2)
    #data = str(pump())         # data = return value of pump function
    q.put(data)
    
# speaker process
#def speaker_worker():
    # speaker

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
