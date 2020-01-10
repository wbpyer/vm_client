import multiprocessing
import socket
import time
from multiprocessing import Process
from threading import Thread
# from vm.test.test02 import check_port

work= True

def check_port(ip, port=3389):
    while work:
        time.sleep(5)
        s = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)

        try:

            s.connect((ip, port))

            s.shutdown(2)

            print('%s:%d is used' % (ip, port))

            work = False

        except socket.error as e:

            print('%s:%d is unused' % (ip, port))


        time.sleep(2)



def _test():
    while work:
        time.sleep(2)
        print("00000()00000")




    # p = Process(target=check_port,args=("127.0.0.1",))
p = Thread(target=check_port,args=("127.0.0.1",))
p1= Thread(target=_test)
p.start()
p1.start()
    #
    # p.join()
print("_______________")

while work:
    time.sleep(2)
    print("123321")
    # a = input("input:")
    # if a == 'quit':
    #     work = False

