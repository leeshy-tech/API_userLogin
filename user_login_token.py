'''用户登陆API
增加：token验证
url1:http://127.0.0.1:8899/users/login
url2:http://127.0.0.1:8899/users/info
'''

from flask import Flask,request,jsonify
from flask_cors import CORS
from gevent import pywsgi
import time
import jwt

port = 8899
app = Flask(__name__)
CORS(app,resource=r'/*')

# 加密算法
headers = {
    "alg":"HS256",
    "typ":"JWT"
}
# 密钥
SECRET_KEY = "leeshy"

users_list = [
    {"user_id":"2019210777","user_password":"123456"},
    {"user_id":"2019210778","user_password":"123456"},
    {"user_id":"2019210779","user_password":"123456"}
]

users_headphotos = [
    {"user_id":"2019210777","user_headphoto":"http://8.136.83.196:8080/pictures/headphoto1.jpeg"},
    {"user_id":"2019210778","user_headphoto":"http://8.136.83.196:8080/pictures/headphoto2.jpeg"},
    {"user_id":"2019210779","user_headphoto":"http://8.136.83.196:8080/pictures/headphoto3.jpeg"}
]

'''生成一个token'''
def token_encode(user_id) -> str:
    if user_id:
        payload = {
            "user_id":user_id
        }
        token = jwt.encode(payload=payload, key=SECRET_KEY,algorithm='HS256',headers=headers)
        return token
    else:
        return None

'''解码token'''
def token_decode(token) -> str:
    payload = jwt.decode(jwt=token,key=SECRET_KEY,verify=False,algorithms='HS256')
    info = payload["user_id"]
    return info

'''生成一个返回体'''
def response_body_login(msg,user_id=None):
    response_msg = [
        {"msg":msg},
        {"token":token_encode(user_id)}
    ]
    return jsonify(response_msg)

'''
用户登陆
请求体示例：
{
    {"user_id":"2019210777"},
    {"user_password":"123456"}
}
'''
@app.route('/users/login',methods=['POST'])
def users_login():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        user_password = request.form.get("user_password")

        for user_dict in users_list:
            if user_dict["user_id"] == user_id:
                if user_dict["user_password"] == user_password:
                    return response_body_login("success",user_id)
                else: 
                    return response_body_login("password error")

        return response_body_login("id not exist")

'''
获取用户信息（简化版，只有头像对应的网络链接）
请求体：
头部加入"token":token
'''
@app.route('/users/info',methods=['POST'])
def users_info():
    if request.method == "POST":
        token = request.headers["token"]
        try:
            user_id = token_decode(token)
        except:
            return "token error"

        for user_dict in users_headphotos:
            if user_dict["user_id"] == user_id:
                return user_dict["user_headphoto"]

        return "no headphoto"


if __name__ == "__main__":
    server = pywsgi.WSGIServer(('0.0.0.0',port),app)
    server.serve_forever()
    print("end")