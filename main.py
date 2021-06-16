from ui_main import *
from temp import *
from multiprocessing import Queue, Process, Manager

if __name__ == "__main__":
    Manager = Manager()
    SharedMemory = Manager.list()
    f = open('default.txt', 'r')
    for _ in range(5):
        SharedMemory.append(eval(f.readline()))  # now_temp, target_temp, beer_percent, amount_per_sec_mac, amount_per_sec_sso
    f.close()

    p1 = Process(name="ui_main", target=ui_main, args=(SharedMemory, ))
    time.sleep(1)
    p2 = Process(name="temp_main", target=temp_main, args=(SharedMemory, ))
    p1.start()
    p2.start()
    i = 0
    while True:
        if not (p1.is_alive()) and p2.is_alive():
            p2.kill()
            time.sleep(1)
            break
            
        '''
        while i < 3:
            if not(p1.is_alive()) and p2.is_alive():
                time.sleep(1)
                p1 = Process(name="ui_main", target=ui_main, args=(SharedMemory,))
                p1.start()
                i += 1
        '''





