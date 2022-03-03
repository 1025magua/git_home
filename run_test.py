"""
-------------------------------------------------
   File Name:run_test35
   Author:Lee
   date: 2021/9/24-10:53
-------------------------------------------------
"""

import unittest
from BeautifulReport import BeautifulReport
from comms.constants import CASE_DIR, REPORT_DIR

"""
HTML类型的结果报告
# 1.下载BeautifulReport包
# 2.在代码中 import 该模块
"""

# 1.创建测试套件(测试套件的作用:我们可以把需要运行的测试案例，添加到测试套件中)
suite = unittest.TestSuite()

# 2.3 添加整个目录下的测试类到测试套件中,注意：测试模块必须以test开头
loader = unittest.TestLoader()
suite.addTest(loader.discover(CASE_DIR))

# 3.使用BeautifulReport 运行测试套件
BeautifulReport(suite).report(description='tester21班接口自动化测试报告',
                              filename='report',
                              report_dir=REPORT_DIR)
