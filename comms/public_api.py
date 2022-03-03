"""
-------------------------------------------------
   File Name:public_api
   Author:Lee
   date: 2021/9/30-10:54
-------------------------------------------------
"""
import requests
from configparser import ConfigParser
from comms.constants import CONF_FILE


# 从ini文件获取数据
def get_ini_data(section, option):
    try:
        cnp = ConfigParser()
        cnp.read(CONF_FILE, encoding='utf-8')
        return cnp.get(section, option)
    except Exception as e:
        print('从ini文件读取测试数据失败！', e)


# 获取token值
def get_token():
    try:
        response = requests.post(url='http://127.0.0.1:6666/business/token_login',
                                 data={"username": get_ini_data('user2', 'name'),
                                       "password": get_ini_data('user2', 'password'),
                                       "typeId": '101'})
        res_body = response.json()
        return res_body['token']
    except Exception as e:
        print('获取token值失败!', e)


# 数据替换
def replace_data(my_dict, key, value):
    """
    :param my_dict: 需要替换的字符串类型的字典
    :param key: 需要替换的key
    :param value: 替换的数据
    :return: 替换后的字符串类型的字典
    """
    dict1 = eval(my_dict)
    dict1[key] = value
    return str(dict1)


if __name__ == '__main__':
    # data = get_ini_data('mysql', 'host')
    # print(data)
    #
    # print(get_token())

    a = '{"username": "xiaohua", "password": "a123456", "token": "daskjldbgaslhad"}'

    print(replace_data(a, 'token', '789'))
