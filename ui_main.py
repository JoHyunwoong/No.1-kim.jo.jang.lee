from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from ui_version5 import Ui_MainWindow
from sys import exit, argv
from threading import Thread
from pump import *
from buzzer import *
from ui_functions import UIFunctions
from temp import *
from queue import Queue


class MainWindow(UIFunctions):
    def __init__(self, error_code_queue, SharedMemory):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.error_code_queue = error_code_queue
        self.SharedMemory = SharedMemory
        self.is_moving = False
        self.isFirst1 = 1
        self.isFirst2 = 1
        self.isReplay1 = 0
        self.isReplay2 = 0
        self.now_temp = SharedMemory[0]
        self.target_temp = SharedMemory[1]
        self.consumer = Consumer(self.error_code_queue, SharedMemory)
        self.consumer.poped1.connect(self.show_popup)
        self.consumer.poped2.connect(self.update_temperature)
        self.consumer.start()
        self.beer_percent = self.SharedMemory[2]
        self.amount_sso = 360
        self.amount_mac = 500
        self.sso_2nd = 0
        self.mac_2nd = 0
        self.buzzer_tone_number = 1
        self.amount_per_sec_sso = self.SharedMemory[3]  # output of sso pump per second
        self.amount_per_sec_mac = self.SharedMemory[4]  # output of mac pump per second
        self.ui.now_temperature_qlcd.display(str(self.now_temp))
        self.ui.set_temperature_qlcd.display(str(self.target_temp))
        self.ui.pump1_parameter.display(str(self.amount_per_sec_sso))
        self.ui.pump2_parameter.display(str(self.amount_per_sec_mac))
        self.ui.set_temperature_up_button.clicked.connect(self.temperature_up)
        self.ui.set_temperature_down_button.clicked.connect(self.temperature_down)
        self.ui.beer_slider.setValue(self.beer_percent)
        self.ui.beer_slider.valueChanged.connect(self.update_prograssbar)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        self.ui.comboBox.currentIndexChanged.connect(self.buzzer_tone_select)
        self.ui.btn_back.clicked.connect(self.showpage)
        self.ui.btn_home.clicked.connect(self.showhomepage)
        self.ui.btn_monitor.clicked.connect(self.showmonitor)
        self.ui.btn_parameter.clicked.connect(self.showparameter)
        self.ui.btn_settings.clicked.connect(self.showsetting)
        self.ui.drink1_replace_button.clicked.connect(self.replace_drink1)
        self.ui.drink2_replace_button.clicked.connect(self.replace_drink2)
        self.ui.start_button.clicked.connect(self.makestart)
        self.ui.pushButton.clicked.connect(self.save_default)
        self.ui.pump1_parameter_up01.clicked.connect(lambda: self.pump1_parameter_calculate(0.1))
        self.ui.pump1_parameter_up05.clicked.connect(lambda: self.pump1_parameter_calculate(0.5))
        self.ui.pump1_parameter_down01.clicked.connect(lambda: self.pump1_parameter_calculate(-0.1))
        self.ui.pump1_parameter_down05.clicked.connect(lambda: self.pump1_parameter_calculate(-0.5))
        self.ui.pump2_parameter_up01.clicked.connect(lambda: self.pump2_parameter_calculate(0.1))
        self.ui.pump2_parameter_up05.clicked.connect(lambda: self.pump2_parameter_calculate(0.5))
        self.ui.pump2_parameter_down01.clicked.connect(lambda: self.pump2_parameter_calculate(-0.1))
        self.ui.pump2_parameter_down05.clicked.connect(lambda: self.pump2_parameter_calculate(-0.5))

        self.show()

    # 창 드래그이동
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_moving = True
            self.ui.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_moving:
            self.move(event.globalPos() - self.ui.offset)

    # 스타트기능
    def makestart(self):  # 제조시작
        self.ui.start_button.setEnabled(False)  # 중복실행을 위해 버튼 비활성화
        p1 = Thread(target=self.worker)
        p1.start()

    # pump worker
    def worker(self):
        rate = (100 - int(self.ui.beer_slider.value())) / 100
        print(rate)
        isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd, isError = \
            pumpAlcohol(rate, self.isFirst1, self.isReplay1, self.amount_sso, self.sso_2nd,
                        self.amount_per_sec_sso, self.isFirst2, self.isReplay2,
                        self.amount_mac, self.mac_2nd, self.amount_per_sec_mac)
        if isError == 7:
            self.error_code_queue.put(isError)
        else:
            self.isFirst1, self.isReplay1, self.amount_sso, self.sso_2nd, self.isFirst2, self.isReplay2, self.amount_mac, self.mac_2nd \
                = isFirst1, isReplay1, amount_sso, sso_2nd, isFirst2, isReplay2, amount_mac, mac_2nd
            self.error_code_queue.put(isError)
            print(isError, self.amount_sso, self.amount_mac)  # test print
            if not(isError == 1 or isError == 2) and str(self.ui.comboBox.currentText()) == "소리 켜기":
                print("부저 작동")
                buzzer()



    def update_temperature(self, data):
        self.now_temp = round(data, 2)
        self.ui.now_temperature_qlcd.display(str(self.now_temp))


# read q and connect thread
class Consumer(QThread):
    poped1 = pyqtSignal(int)
    poped2 = pyqtSignal(float)

    def __init__(self, q, SharedMemory):
        super().__init__()
        self.q = q
        self.SharedMemory = SharedMemory

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.poped1.emit(data)
            data = self.SharedMemory[0]
            self.poped2.emit(data)
            time.sleep(1)


def ui_main(SharedMemory):
    error_code_queue = Queue()
    app = QApplication(argv)
    main_win = MainWindow(error_code_queue, SharedMemory)
    exit(app.exec_())


if __name__ == '__main__':
    ui_main()
