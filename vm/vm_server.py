
from flask import Flask,request
from vm.vm_main import Vmare
from flask_mail import Mail, Message
from flask_cors import CORS



app = Flask(__name__)
CORS(app)  # 允许跨站访问
app.config.update(
    DEBUG = False,
    MAIL_SERVER='smtp.qq.com',
    MAIL_PROT=465,
    MAIL_USE_TLS = True,
    MAIL_USERNAME = '63285625@qq.com',
    MAIL_PASSWORD = 'wb15049082567c',
)



@app.route('/vm',methods=['POST'])
def vm_data():
    """
    接受用户的信息，以及token,对token做一个验证，然后解析数据。验证成功才能继续下一步，
    :return:
    """
    # msg = Message("wanring", sender='63285625@qq.com', recipients=['shengjun@itcast.cn', '371673381@qq.com'])
    #payload = {'user_name': user_name, 'user_id': user_id, 'payload': payload}
    # d = request.body
    data = request.json


    user_name = data.get('user_name')
    user_id = data.get('user_id')
    payload = data.get('payload')

    try:



        vm = Vmare(payload,user_id,user_name)    #初始化测试成功，对数据合理解析
        print(vm.payload)
        print(vm.db_name)
        print(vm.leader_db_name)

        vm.start()


        vm.working() # 单元测试2成功   接下来需要配合数据库，开发数据库端  联合数据库测试成功

        #等待用户退出虚拟机时，调用下面这个，这个信号，应该是运维给的，中间用户会有工作的时间。
        # time.sleep(15)

        vm.exit()  # 业务没问题，需要数据库配合。  联合数据库测试成功


    except Exception as e:
        # msg.body = "虚拟机端出现异常:{}".format(e)
        # mail.send(msg)

        print("记录日志，通知运维 我是最外层程序 错误:{0}".format(e))
    #在这里记录日志，里面就不用记录了。


    return "ok"

if __name__ == '__main__':
    print(app.url_map)
    app.run(host = '127.0.0.1',port=5001)



