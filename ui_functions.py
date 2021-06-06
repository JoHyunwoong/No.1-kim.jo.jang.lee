from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QPropertyAnimation
from PyQt5.QtWidgets import QMessageBox


class UIFunctions(QMainWindow):
    def __init__(self):
        super().__init__()

    # 페이지 전환 기능
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

    # 최소화 버튼
    def show_minimized(self):
        self.ui.showMinimized()

    def replace_drink1(self):
        self.amount_sso = 360
        self.ui.drink1_progressbar.setValue(self.amount_sso/360 * 100)
        self.ui.drink1_residual_label.setText(str(self.amount_sso))

    def replace_drink2(self):
        self.amount_mac = 500
        self.ui.drink2_progressbar.setValue(self.amount_mac/500 * 100)
        self.ui.drink2_residual_label.setText(str(self.amount_mac))

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
            self.ui.drink1_residual_label.setText(str(int(self.amount_sso)))
            self.ui.drink2_residual_label.setText(str(int(self.amount_mac)))
            self.ui.drink1_progressbar.setValue(self.amount_sso/360 * 100)
            self.ui.drink2_progressbar.setValue(self.amount_mac/500 * 100)
        self.ui.start_button.setEnabled(True)
