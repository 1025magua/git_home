"""
-------------------------------------------------
   File Name:test_login01
   Author:Lee
   date: 2021/9/30-10:53
-------------------------------------------------
"""
import pytest
import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.db_utils import DBUtils
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
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, '登录')

    @allure.severity("critical")
    @allure.description("商品登录模块接口测试用例")
    @pytest.mark.parametrize("case", cases)
    def test_login(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='请求参数')

        uname = eval(case.case_data)['username']
        passwd = eval(case.case_data)['password']
        # 正确流程
        if case.case_id == 1:
            self.db.cud('delete from tb_user where name = %s or email = %s or phone = %s',
                        (uname, 'tester21@163.com', '19988775544'))
            self.db.cud('insert into tb_user(name,passwd,email,phone) values(%s,%s,%s,%s)',
                        (uname, passwd, 'tester21@163.com', '19988775544'))
        elif case.case_id == 3:  # 用户名不存在的场景
            self.db.cud('delete from tb_user where name = %s', (uname,))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()
        allure.attach(body=str(res_body), name='响应参数')

        try:
            if case.case_id == 1:
                assert case.expect in str(res_body)
            else:
                assert eval(case.expect) == res_body  # assert是断言的意思，Equal是相等、比较的意思
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, '登录', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败！实际结果:{}'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, '登录', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功！'.format(case.case_id, case.case_title))


if __name__ == '__main__':
    pytest.main(["-vs", '--tb=line', "./test_login03.py"])
