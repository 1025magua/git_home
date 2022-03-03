"""
-------------------------------------------------
   File Name:constants
   Author:Lee
   date: 2021/9/29-17:31
-------------------------------------------------
"""

import os

# 获取项目路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# print(BASE_DIR)  # D:/PythonWorkSpace/autotest02

# 测试用例执行文件所在路径
CASE_DIR = os.path.join(BASE_DIR, 'testcases')
# print(CASE_DIR)

# 测试数据所在路径
DATA_DIR = os.path.join(BASE_DIR, 'datas')
DATA_FILE = os.path.join(DATA_DIR, 'cases.xlsx')
# print(DATA_FILE)

# log所在路径
LOG_DIR = os.path.join(BASE_DIR, 'logs')
INFO_FILE = os.path.join(LOG_DIR, 'info.log')
ERROR_FILE = os.path.join(LOG_DIR, 'error.log')

# 配置文件所在路径
CONF_DIR = os.path.join(BASE_DIR, 'conf')
CONF_FILE = os.path.join(CONF_DIR, 'config.ini')

# 测试报告所在路径
REPORT_DIR = os.path.join(BASE_DIR, 'reports')
