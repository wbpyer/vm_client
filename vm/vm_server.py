import logging
from flask import Flask,request,jsonify
from vm.vm_main import Vmare
from flask_cors import CORS
import requests



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

        """
        根据不同的情况调用不同的退出，目前工区和普通人员走一个退出通道就行。"""
        # if Vmare._instance.role in["安全管理报表","现场管理报表","经营管理报表","物资设备管理报表"]:
        #     app.logger.error("退出程序已经启动")
        #     Vmare._instance.WORK_group = False
        #     Vmare._instance.exit_group()
        # else:
        if Vmare._instance.is_leader == 1:
            Vmare._instance.exit2()

        else:

            Vmare._instance.WORK = False
            app.logger.error("退出程序已经启动")
            Vmare._instance.exit()
            print(Vmare._instance)


        return "exit is OK", 200


    except Exception as e:
        app.logger.error("退出程序发生错误 s% ",e)
        return "exit exception", 409

    # except File_exists_error as e:
    #     print('通知文件没有删除干净,运维登录删除文件')
    #     return "need human help clean dir", 405


    # except Exception as e:
    #
    #     print(e)
    #
    #     app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)
    #     # todo 启动Redis还原程序 还原程序待开发,以后可以在开发，目前先不考虑，不急。证明没用通知到毕工，再次请求毕工
    #
    #     print('先启动还原，然后再次请求毕工')
    #
    #     addrs = socket.getaddrinfo(socket.gethostname(), None)
    #     data = {"ip": [item[4][0] for item in addrs if ':' not in item[4][0]][0]}
    #     print(data)
    #
    #     resp = requests.post('http://10.0.0.2:9999/endvm', json=data)
    #     #没有返回时间，这里就不会报错。
    #     print(resp.text)
    #
    #
    #     return "file is fail,but i had conn bi_exit ", 409
    #     #需要毕工调度起来我的错误处理程序。


@app.route('/vm/work',methods=['GET'])
def vm_working():
    """
    项目部公司人员走的接口。
    :return:
    """


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
    # templater = data.get('templater')   # 点击不同的功能，切换不同的模板。
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

    #如过这是领导要看，就走这个逻辑，一个单独的逻辑，这里面的模块交给了王倩。

    try:
        if vm.is_leader == 0:


            requests.get("http://127.0.0.1:5000/vm/work",timeout=1)
        else:
            requests.get("http://127.0.0.1:5000/vm/work2", timeout=1)

    except Exception as e:
        print("我自己起了文件监控程序".format(e))


    return 'ok'


@app.route('/vm/work2',methods=['GET'])
def vm_working2():
    # 先去下载登录的这个人的zip
    # 然后再去下载下属每个人的zip，最后将所有下属的zip合并到登录的人的zip中解压加载

    try:
        print('来了~~~~~~~~~~~~~~~~~~~~~~')
        # start之前已经
        Vmare._instance.start2()

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





@app.route('/vm/group',methods=['GET'])
def group():
    """
    工区人员走的接口。
    :return:
    """


    try:
        #工区也是这个start 但是working会不一样。
        Vmare._instance.start()

        Vmare._instance.working2group()



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
















