import logging
from flask import Flask,request,jsonify
from vm.vm_main import Vmare
from flask_cors import CORS





app = Flask(__name__)
CORS(app)  # 允许跨站访问


@app.route('/vm/exit',methods=['POST'])
def vm_exit():
    """
    退出时，毕工请求这个地址。虚拟机端将执行退出过程。
    # todo 和毕工接口1
    :return:
    """
    try:

        Vmare._instance.WORK = False
        print(Vmare._instance)
        return "exit is OK", 200

    except Exception as e:
        print(e)
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        return "exit is fail", 404


@app.route('/vm',methods=['POST'])
def vm_data():
    """
    接受用户的信息，然后解析数据。验证成功才能继续下一步，
    一旦成功解析数据，开始调用虚拟机实例各种方法。
    :return:
    """

    try:

        data = request.json
        user_name = data.get('user_name')
        user_id = data.get('user_id')
        payload = data.get('payload')
        vm = Vmare(payload, user_id, user_name)
        print(vm.payload)
        print(vm.db_name)
        print(vm.leader_db_name)

        vm.start()

        vm.working() # 单元测试2成功   接下来需要配合数据库，开发数据库端  联合数据库测试成功
        #等待用户退出虚拟机时，调用下面这个，这个信号，应该是运维给的，中间用户会有工作的时间。
        # 上面会阻塞主，用户一直在虚拟机上工作。直到由运维将请求发送给，退出接口，才会执行下面的工作。

        vm.exit()

        return "ok",200
    except Exception as e:

        print("记录日志，通知运维 我是最外层程序 错误:{0}".format(e))
        app.logger.error("error_msg: %s remote_ip: %s user_agent: %s ",e,request.remote_addr,request.user_agent.browser)

        res = {'status': 404, "data": "无法初始化数据"}
        return jsonify(res),404

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
    handler = logging.FileHandler('C:\\logs\\vm_server.log', encoding='UTF-8')
    handler.setLevel(logging.DEBUG)
    logging_format = logging.Formatter("%(asctime)s app:flask fun:%(funcName)s %(levelname)s %(message)s")
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)
    app.run(host = '0.0.0.0',port=5001)




