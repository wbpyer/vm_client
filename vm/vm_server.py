from flask import Flask,request
from flask_cors import CORS
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from vm.vm.vm_main import Vmare




app = Flask(__name__)
CORS(app)
SERECT_KEY = 'fdjsklafjkldsja'  #密匙 ，权限那里给的。
Ser = Serializer(SERECT_KEY)





@app.route('/vm',methods=['POST'])
def vm_data():
    """
    接受用户的信息，以及token,对token做一个验证，然后解析数据。验证成功才能继续下一步，
    :return:
    """

    #验证token，解析数据，开启虚拟机类里面的方法。
    data = request.form
    token = data.get('token')

    try:

        payload = Ser.loads(token)

    except Exception as e:
        print(e,'记录日志')
        return "验证未通过，无法为您准备工作区,下面代码就不在执行了"


    try:
        user_name = data.get('user_name')
        user_id = data.get('user_id')

        vm = Vmare(payload,user_name,user_id)

        vm.start()
        vm.working()

        #等待用户退出虚拟机时，调用下面这个，这个信号，应该是运维给的，中间用户会有工作的时间。
        vm.exit()


    except Exception as e:
        print("记录日志，通知运维")
    #在这里记录日志，里面就不用记录了。


    return "ok"

if __name__ == '__main__':
    app.run(host = '127.0.0.1',port=5000)


