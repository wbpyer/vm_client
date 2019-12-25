import logging
from flask import Flask,request,jsonify
from vm.vm_main import Vmare
from flask_cors import CORS
from vm.vm_error import Timeout
import requests
import socket



app = Flask(__name__)
CORS(app)  # 允许跨站访问



@app.route('/vm/exit',methods=['POST'])
def vm_exit():
    """
    退出时，毕工请求这个地址。虚拟机端将执行退出过程。
    # todo 和毕工接口1
    :return:
    """
    app.logger.error("bi_come_in_exit_now_remote_ip: %s user_agent: %s ", request.remote_addr, request.user_agent.browser)



    try:

        Vmare._instance.WORK = False
        app.logger.error("退出程序已经启动")
        Vmare._instance.exit()
        print(Vmare._instance)


        return "exit is OK", 200



    except Timeout as e:
        return "exit is OK", 200




    # except File_exists_error as e:
    #     print('通知文件没有删除干净,运维登录删除文件')
    #     return "need human help clean dir", 405


    except Exception as e:

        print(e)

        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
        # todo 启动Redis还原程序 还原程序待开发,以后可以在开发，目前先不考虑，不急。证明没用通知到毕工，再次请求毕工

        print('先启动还原，然后再次请求毕工')

        addrs = socket.getaddrinfo(socket.gethostname(), None)
        data = {"ip": [item[4][0] for item in addrs if ':' not in item[4][0]][0]}
        print(data)

        resp = requests.post('http://10.0.0.2:9999/endvm', json=data)
        #没有返回时间，这里就不会报错。
        print(resp.text)


        return "file is fail,but i had conn bi_exit ", 409
        #需要毕工调度起来我的错误处理程序。




@app.route('/vm/work',methods=['GET'])
def vm_working():


    try:

        Vmare._instance.start()

        Vmare._instance.working()
        # 单元测试2成功   接下来需要配合数据库，开发数据库端  联合数据库测试成功
            #等待用户退出虚拟机时，调用下面这个，这个信号，应该是运维给的，中间用户会有工作的时间。
            # 上面会阻塞主，用户一直在虚拟机上工作。直到由运维将请求发送给，退出接口，才会执行下面的工作。

            # vm.exit()

        return "ok",200
    except Exception as e:

        print("i am outside layer error is:{0}".format(e))
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        res = {'status': 405, "data": "error is:{0}".format(e)}
        return jsonify(res),405



@app.route('/vm',methods=['POST'])
def vm_start():
    """
    接受用户的信息，然后解析数据。验证成功才能继续下一步，
    一旦成功解析数据，开始调用虚拟机实例各种方法。
    :return:
    """



    data = request.json
    user_name = data.get('user_name')
    user_id = data.get('user_id')
    payload = data.get('payload')
    vm = Vmare(payload, user_id, user_name)
    print(vm.payload)
    app.logger.error(" dbname: %s remote_ip: %s user_agent: %s ", vm.db_name, request.remote_addr,
                     request.user_agent.browser)
    print(vm.db_name)
    app.logger.error(" leaderdbname: %s remote_ip: %s user_agent: %s ", vm.leader_db_name, request.remote_addr,
                     request.user_agent.browser)
    print(vm.leader_db_name)

    try:
        requests.get("http://127.0.0.1:5000/vm/work",timeout=1)
    except Exception as e:
        print(e)

    return 'ok'

    #在这里记录日志，里面就不用记录了。


@app.route('/vm/health',methods=['POST','GET'])
def vm_health():
    """
    健康检查接口，心跳监测，判断服务是否活着。
    :return:
    """

    return "ok",200






if __name__ == '__main__':
    print(app.url_map)
    handler = logging.FileHandler('C:\\logs\\vmnew.txt', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host = '0.0.0.0',port=5000)












