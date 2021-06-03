from ui_main import *


class UIFunctions(MainWindow):

    # 페이지 기능
    def showhomepage(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)
        self.ui.label_top_info_2.setText("HOME")
    def showmonitor(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_monitor)
        self.ui.label_top_info_2.setText("MONITOR")
    def showsetting(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_settings)
        self.ui.label_top_info_2.setText("SETTING")
    def toggleMenu(self, maxWidth, enable):  # 토글기능구현
        if enable:

            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 70

            if width == 70:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(400)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.start()

    def show_minimized(self):
        """버튼 명령: 최소화"""
        self.ui.showMinimized()



    # 오류 팝업     poped1 연결
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
            self.ui.display_remains1.display(str(int(self.amount_sso)))     # 소수점 제거
            self.ui.display_remains2.display(str(int(self.amount_mac)))     # 소수점 제거
        self.ui.start_btn.setEnabled(True)