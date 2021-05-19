from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPropertyAnimation
from ui_version1 import Ui_MainWindow
import sys
import time
from threading import Thread


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.first_percent = 30         # 초기값 설정
        self.second_percent = 70

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
        self.thread1 = Thread(target=self.make_process)
        self.thread1.start()

    def make_process(self):     # 제조과정
        self.ui.start_btn.setEnabled(False)     # 중복실행을 위해 버튼 비활성화
        '''return_value = function()             # 함수 실행
        if return_value == 1:
            display error  popup
        else if return_value == 2:
            display amount shortage popup
        else if return_value == 0:
            speaker '''
        self.ui.start_btn.setEnabled(True)

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

# 실행
if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys.exit(app.exec_())