"""
-------------------------------------------------
   File Name:test_business_register01
   Author:Lee
   date: 2021/10/5-9:24
-------------------------------------------------
"""
import requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.db_utils import DBUtils
import pytest
import allure

"""
1.主流程
2.数据回滚
3.追加其它用例
"""


@allure.feature("商品注册模块")
class TestRegister:

    @pytest.fixture(autouse=True)
    def connect_db(self):
        self.db = DBUtils()
        yield
        self.db.close()

    cases = ReadExcel.read_data_all(DATA_FILE, '注册')

    @allure.severity("critical")
    @allure.description("商品注册模块接口测试用例")
    @pytest.mark.parametrize("case", cases)
    def test_register(self, case):
        allure.dynamic.title(case.case_title)
        allure.attach(body=case.url, name='接口路径')
        allure.attach(body=case.case_data, name='接口参数')

        uname = eval(case.case_data)["username"]
        email = eval(case.case_data)["email"]
        phone = eval(case.case_data)["phone"]
        # 正确流程
        if case.case_id in (1, 2, 3, 4, 5):
            self.db.cud('delete from tb_user where name = %s or email = %s or phone = %s', (uname, email, phone))
        if case.case_id == 13:  # 用户名已存在，但手机号和邮箱不重复的场景
            self.db.cud('delete from tb_user where name = %s or email = %s or phone = %s', (uname, email, phone))
            self.db.cud('insert into tb_user(name,passwd,email,phone) values(%s,%s,%s,%s)',
                        (uname, 'test123456', 'tester21@qq.com', '17677777777'))
        if case.case_id == 22:  # 手机号已存在，但用户名和邮箱不重复的场景
            self.db.cud('delete from tb_user where name = %s or email = %s', (uname, email))
        if case.case_id == 32:  # 邮箱已存在，但用户名和手机号不重复的场景
            self.db.cud('delete from tb_user where name = %s or phone = %s', (uname, phone))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()
        allure.attach(body=str(res_body), name='响应结果')

        try:
            assert eval(case.expect) == res_body
            # 数据验证
            if case.case_id in (1, 2, 3, 4, 5):
                count = self.db.find_count('select * from tb_user where name = %s', (uname,))
                assert 1 == count

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, '注册', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, '注册', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))
