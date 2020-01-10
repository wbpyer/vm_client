import sys, socket
import time
# from vm.test.test_process import work



def check_port(ip, port=3389):
    while work:
        s = socket.socket(socket.AF_INET ,socket.SOCK_STREAM)

        try:

            s.connect((ip, port))

            s.shutdown(2)

            print('%s:%d is used' % (ip, port))



        except socket.error as e:

            print('%s:%d is unused' % (ip, port))


        time.sleep(2)


if __name__ == '__main__':
    # args = sys.argv
    #
    # port = sys.argv[1]



    # parser=OptionParser()

    # parser.add_option('-a', '--addr', dest='addr', help='')

    # parser.add_option('-p', '--port', dest='port', default=80, type="int", help='')

    # (options, args) = parser.parse_args()

    # print "options===>", options.addr, args

    # parser = ArgumentParser(description="TCP端口检测")
    #
    # parser.add_argument('a1')  # 输入参数时候不用字典传参。
    #
    # parser.add_argument('-o', '--other', dest='other')  # 输入参数时候需要字典传参，python test.py 33 -o56 127.0.0.1 3306
    #
    # parser.add_argument('-a', '--addr', dest='addr', default='localhost', help='address for the server')
    #
    # parser.add_argument('-p', '--port', dest="port", default=80, type=int, choices=[80, 443, 3306],
    #                     help='port for the server')

    # args = parser.parse_args()

    # args = parser.parse_known_args()[0]

    # print("args===>", args, args.port)

    result = check_port("127.0.0.1",3389)
    print(result)
    sys.exit(0)