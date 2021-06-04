from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication
from PyQt5.QtCore import QPropertyAnimation, QThread, pyqtSignal, QRect, Qt
from ui_version4 import Ui_MainWindow
from sys import exit, argv
from threading import Thread
from pump import *
from multiprocessing import Queue, Process
from ui_functions import *

class MainWindow(QMainWindow):
    def __init__(self, q, t):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.is_moving = False
        self.q = q
        self.t = t
        self.consumer = Consumer(self.q, t)
        self.consumer.poped1.connect(lambda: UIFunctions.show_popup)
        #self.consumer.poped2.connect(self.update_temperature)
        self.consumer.start()
        self.beer_percent = 70
        self.amount_sso = 360
        self.amount_mac = 500
        self.temperature = 0

        self.ui.btn_close.clicked.connect(lambda: self.close())
        self.ui.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.ui.beer_slider.setValue(self.beer_percent)
        self.ui.beer_progressbar.setValue(self.beer_percent)
        self.ui.beer_slider.valueChanged.connect(self.ui.beer_progressbar.setValue)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        self.ui.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))
        self.ui.btn_home.clicked.connect(lambda: UIFunctions.showhomepage(self))
        self.ui.btn_monitor.clicked.connect(lambda: UIFunctions.showmonitor(self))
        self.ui.btn_settings.clicked.connect(lambda: UIFunctions.showsetting(self))

        self.ui.start_button.clicked.connect(self.makestart)

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
        p1 = Thread(target=self.worker, args=(self.q,))
        p1.start()


    # pump worker
    def worker(self, q):
        pump_error_value, self.amount_sso, self.amount_mac = pumpAlcohol((100 - self.beer_percent)/100, self.amount_sso, self.amount_mac)
        print(pump_error_value, self.amount_sso, self.amount_mac) # test print
        q.put(str(pump_error_value))
        #if pump_error_value == 0:
            #buzzer()

#def producer(t):
   # while True:
        #data = displayTemp()
        #t.put(data)
        #time.sleep(1)


# read q and connect thread
class Consumer(QThread):
    poped1 = pyqtSignal(str)
    poped2 = pyqtSignal(int)

    def __init__(self, q, t):
        super().__init__()
        self.q = q
        self.t = t

    def run(self):
        while True:
            if not self.q.empty():
                data = self.q.get()
                self.poped1.emit(data)
            if not self.t.empty():
                data = self.t.get()
                self.poped2.emit(data)
            time.sleep(1)

def main():
    q = Queue()
    t = Queue()
    #p = Process(name="producer", target=producer, args=(t,), daemon=True)
    #p.start()
    app = QApplication(argv)
    main_win = MainWindow(q, t)
    exit(app.exec_())

if __name__ == '__main__':
    main()
'''
if __name__ == '__main__':
    q = Queue()

    app = QApplication(sys.argv)
    main_win = MainWindow(q)
    sys.exit(app.exec_())
    '''
