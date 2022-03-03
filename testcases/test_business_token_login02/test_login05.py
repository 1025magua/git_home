"""
-------------------------------------------------
   File Name:test_login01
   Author:Lee
   date: 2021/9/30-10:53
-------------------------------------------------
"""

import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.db_utils import DBUtils
from comms.public_api import replace_data
import pytest
import allure

"""
1.主流程
2.数据回滚
3.追加其它用例
"""


@allure.feature("商品登录模块")
class TestLogin:

    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        one = self.db.find_one('select * from tb_user order by rand() limit 1;')
        self.name, self.pwd = one[1], one[2]
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, '登录1')

    @allure.severity("critical")
    @allure.description("商品登录模块接口测试用例")
    @pytest.mark.parametrize('case', cases)
    def test_login(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')

        if '#name#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'username', self.name)
            if case.case_id == 4:  # 用户名区分大小写
                case.case_data = replace_data(case.case_data, 'username', self.name.upper())
        if '#passwd#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'password', self.pwd)
            if case.case_id == 6:  # 密码区分大小写
                case.case_data = replace_data(case.case_data, 'password', self.pwd.upper())

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()
        allure.attach(body=str(res_body), name='响应结果')

        try:
            if case.case_id == 1:
                assert case.expect in str(res_body)
            else:
                assert eval(case.expect) == res_body  # assert是断言的意思，Equal是相等、比较的意思
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, '登录1', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败！实际结果:{}'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, '登录1', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功！'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(['-vs', '--tb=line', './test_login05.py'])
