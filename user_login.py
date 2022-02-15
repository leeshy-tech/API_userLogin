'''用户登陆API
运行在本机的8899端口
url:http://127.0.0.1:8899/login

请求体示例：
{
    {"user_id":"2019210777"},
    {"user_password":"123456"}
}

响应体示例：
{
    {"msg":"success"}
}

'''

from flask import Flask,request,jsonify
from flask_cors import CORS
from gevent import pywsgi

port = 8899
app = Flask(__name__)
CORS(app,resource=r'/*')

users_list = [
    {"user_id":"2019210777","user_password":"123456"},
    {"user_id":"2019210778","user_password":"123456"},
    {"user_id":"2019210779","user_password":"123456"},
    {"user_id":"2019210780","user_password":"123456"},
    {"user_id":"2019210781","user_password":"123456"}
]

'''生成一个返回体'''
def response_body(msg):
    response_msg = [
        {"msg":msg}
    ]
    return jsonify(response_msg)

@app.route('/login',methods=['POST'])
def func():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_password = request.form.get("user_password")

        for user_dict in users_list:
            if user_dict["user_id"] == user_id:
                if user_dict["user_password"] == user_password:
                    return response_body("success")
                else: 
                    return response_body("password error")

        return response_body("id not exist")

if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',port),app)
    server.serve_forever()
    print("end")