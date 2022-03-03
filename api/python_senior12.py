"""
-------------------------------------------------
   File Name:python_senior11
   Author:Lee
   date: 2021/9/22-17:44
-------------------------------------------------
"""

"""
flask框架介绍:该框架为后端服务框架，能够部署服务，这样我们的接口/代码就能够使用http协议来调用
"""
from comms.db_utils import DBUtils

# 第一步:通过pip install 导入该库
import flask, json

# 第二步:创建app对象,把当前的python文件当成一个服务，__name__代表当前的python的文件
app = flask.Flask(__name__)


# 第三步:将我们接口发布成服务，route是路由的意思
@app.route('/user_login', methods=['get', 'post'])
def login1():
    data = flask.request.values  # 接收请求发送过来的数据
    # print(data)  # CombinedMultiDict([ImmutableMultiDict([('username', 'xiaohu'), ('password', 'a123456')])])
    uname = data.get('username')  # 获取请求中的username对应的值
    pwd = data.get('password')  # 获取请求中的password对应的值

    if len(uname) == 0:
        return json.dumps({"code": 1001, "msg": "用户名不能为空"}, ensure_ascii=False)
    elif len(pwd) == 0:
        return json.dumps({"code": 1002, "msg": "密码不能为空"}, ensure_ascii=False)
    else:  # 查询数据库,看看当前传入的用户名和密码在数据库中是否存在
        db = DBUtils()
        # 从数据库里查询用户名等于 接口传入的用户名 并且密码等于 从接口传入的密码
        count = db.find_count('select * from tb_user where name = %s and passwd = %s', (uname, pwd))
        db.close()
        if count == 0:
            return json.dumps({"code": 1003, "msg": "用户名或密码错误"}, ensure_ascii=False)
        else:
            return json.dumps({"code": 9999, "msg": "登录成功"}, ensure_ascii=False)


# 注册接口
@app.route('/register', methods=['get', 'post'])
def register():
    data = flask.request.values
    uname = data.get('username')
    pwd = data.get('password')
    re_pwd = data.get('re_password')
    email = data.get('email')
    phone = data.get('phone')

    if len(uname) == 0:
        return json.dumps({"code": 1001, "msg": "用户名不能为空"}, ensure_ascii=False)
    elif len(pwd) == 0:
        return json.dumps({"code": 1003, "msg": "密码不能为空"}, ensure_ascii=False)
    elif pwd != re_pwd:
        return json.dumps({"code": 1004, "msg": "两次密码输入不一致"}, ensure_ascii=False)
    elif not (6 <= len(uname) <= 18 and 6 <= len(pwd) <= 18):
        return json.dumps({"code": 1005, "msg": "用户名和密码必须在6-18位之间"}, ensure_ascii=False)
    elif len(email) == 0:
        return json.dumps({"code": 1006, "msg": "邮箱不能为空"}, ensure_ascii=False)
    elif len(phone) == 0:
        return json.dumps({"code": 1007, "msg": "手机号不能为空"}, ensure_ascii=False)
    db = DBUtils()
    count = db.find_count('select * from tb_user where name = %s', (uname,))
    count1 = db.find_count('select * from tb_user where phone = %s', (phone,))
    if count1 != 0 and count == 0:
        db.close()
        return json.dumps({"code": 1008, "msg": "手机号已被注册"}, ensure_ascii=False)
    if count != 0:
        db.close()
        return json.dumps({"code": 1009, "msg": "用户名已存在"}, ensure_ascii=False)
    else:
        cud = db.cud('insert into tb_user(name,passwd,email,phone) values(%s,%s,%s,%s)', (uname, pwd, email, phone))
        db.close()
        if cud == 1:
            return json.dumps({"code": 9999, "msg": "注册成功"}, ensure_ascii=False)
        else:
            return json.dumps({"code": 0000, "msg": "注册失败，环境异常，请联系管理员"}, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True)  # 启动服务(使用debug模式启动服务，debug是可调试模式)
