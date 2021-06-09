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
        self.isFirst = 1
        self.now_temp = SharedMemory[0]
        self.target_temp = SharedMemory[1]
        self.consumer = Consumer(self.error_code_queue, SharedMemory)
        self.consumer.poped1.connect(self.show_popup)
        self.consumer.poped2.connect(self.update_temperature)
        self.consumer.start()
        self.beer_percent = self.SharedMemory[2]
        self.amount_sso = 360
        self.amount_mac = 500
        self.amount_per_sec_mac = self.SharedMemory[3]  # output of mac pump per second
        self.amount_per_sec_sso = self.SharedMemory[4]  # output of sso pump per second
        self.servo = self.SharedMemory[4]
        self.ui.now_temperature_qlcd.display(str(self.now_temp))
        self.ui.set_temperature_qlcd.display(str(self.target_temp))
        self.ui.pump1_parameter.display(str(self.amount_per_sec_sso))
        self.ui.pump2_parameter.display(str(self.amount_per_sec_mac))
        self.ui.set_temperature_up_button.clicked.connect(self.temperature_up)
        self.ui.set_temperature_down_button.clicked.connect(self.temperature_down)
        self.ui.beer_slider.setValue(self.beer_percent)
        self.ui.beer_slider.valueChanged.connect(self.update_prograssbar)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)

        self.ui.btn_back.clicked.connect(self.showpage)
        self.ui.btn_home.clicked.connect(self.showhomepage)
        self.ui.btn_monitor.clicked.connect(self.showmonitor)
        self.ui.btn_parameter.clicked.connect(self.showparameter)
        self.ui.btn_settings.clicked.connect(self.showsetting)
        self.ui.drink1_replace_button.clicked.connect(self.replace_drink1)
        self.ui.drink2_replace_button.clicked.connect(self.replace_drink2)
        self.ui.start_button.clicked.connect(self.makestart)
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
    def makestart(self):        # 제조시작
        self.ui.start_button.setEnabled(False)     # 중복실행을 위해 버튼 비활성화
        p1 = Thread(target=self.worker)
        p1.start()

    # pump worker
    def worker(self):
        pump_error_code, self.amount_sso, self.amount_mac = pumpAlcohol(
            (100 - int(self.ui.beer_slider.value())) / 100, self.amount_sso, self.amount_mac, self.isFirst,
            self.amount_per_sec_mac, self.amount_per_sec_sso)
        if self.isFirst == 1:
            self.isFirst = 0
        print(pump_error_code, self.amount_sso, self.amount_mac)   # test print
        self.error_code_queue.put(pump_error_code)
        #if pump_error_value == 0:
            #buzzer()

    def update_temperature(self, data):
        now_temp = data
        self.ui.now_temperature_qlcd.display(str(round(now_temp, 2)))


# read q and connect thread
class Consumer(QThread):
    poped1 = pyqtSignal(int)
    poped2 = pyqtSignal(int)

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

