"""
-------------------------------------------------
   File Name:test_regist
   Author:Lee
   date: 2021/9/27-16:30
-------------------------------------------------
"""

import requests
import allure
from comms.excel_utils import ReadExcel
from comms.log_utils import logger
from comms.db_utils import DBUtils
from comms.constants import DATA_FILE
import pytest


@allure.feature("注册接口测试")
class TestRegister:
    cases = ReadExcel.read_data_all(DATA_FILE, 'Register')

    @allure.severity("critical")
    @pytest.mark.parametrize("case", cases)
    def test_register(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')

        db = DBUtils()
        # 正确流程
        if case.case_id == 1:
            username = eval(case.case_data)['username']  # 获取传入的用户名
            db.cud('delete from tb_user where name = %s', (username,))
            db.close()

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()
        allure.attach(body=str(res_body), name='响应结果')

        try:
            assert eval(case.expect) == res_body
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'Register', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'Register', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(["-vs", "./test_regist.py"])
