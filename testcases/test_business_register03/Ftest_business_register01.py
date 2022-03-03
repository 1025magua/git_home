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
import pytest

"""
1.主流程
"""


class TestRegister:
    cases = ReadExcel.read_data_pl(DATA_FILE, '注册', 1, 1)

    @pytest.mark.parametrize('case', cases)
    def test_register(self, case):
        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()

        try:
            assert eval(case.expect) == res_body
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, '注册', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, '注册', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))
