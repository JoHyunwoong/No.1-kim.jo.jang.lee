from ui_main import *
from temp import *
from multiprocessing import Queue, Process

if __name__ == "__main__":
    q = Queue()
    t = Queue()
    c = Queue()
    p1 = Process(name="ui_main", target=ui_main, args=(q, t, c))
    p2 = Process(name="temp_main", target=temp_main, args=(t, ))
    p1.start()
    p2.start()
    while True:
        if not c.empty():
            c.get()
            if p2.is_alive():
                p2.kill()
            else:
                p2 = Process(name="temp_main", target=temp_main, args=(t, ))
                p2.start()
            time.sleep(1)
        if not(p2.is_alive() and p1.is_alive()):
            break

    p1.join()
    p2.join()
