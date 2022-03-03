"""
-------------------------------------------------
   File Name:test_login07
   Author:Lee
   date: 2021/9/25-17:34
-------------------------------------------------
"""
import unittest, requests

from ddt import ddt, data
from comms.excel_utils import ReadExcel
from comms.log_utils import logger
from comms.db_utils import DBUtils
from comms.constants import DATA_FILE
import pytest
import allure

cases = ReadExcel.read_data_all(DATA_FILE, 'Login')


@allure.feature("登录接口测试")  # 接口所属模块信息
class TestLogin:  # 测试类需要继承TestCase类，这时当前类就是测试类

    @allure.severity("critical")  # 设置用例优先级
    @allure.description("登录接口")
    @pytest.mark.parametrize("case", cases)
    def test_login(self, case):  # 所有的测试方法必须以test开头
        allure.dynamic.title(case.case_title)  # 动态获取用例名称,allure报告显示用例名称
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')
        # 正确流程
        if case.case_id == 1:
            username = eval(case.case_data)["username"]
            password = eval(case.case_data)["password"]
            db = DBUtils()
            db.cud('delete from tb_user where name = %s', (username,))
            db.cud('insert into tb_user(name,passwd,email,phone) values(%s,%s,%s,%s)',
                   (username, password, 'test@163.com', '18877446699'))
            db.close()

        response = requests.post(url=case.url,
                                 data=eval(case.case_data))  # 识别()中的python表达式，把字符串转成字典
        res_body = response.json()  # res_body就是接口响应的实际结果
        allure.attach(body='{}'.format(res_body), name='响应结果')

        try:
            assert eval(case.expect) == res_body  # assert是断言的意思，Equal是相等、比较的意思
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'Login', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败！实际结果:{}'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'Login', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功！'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(["-vs", "./test_login.py"])
