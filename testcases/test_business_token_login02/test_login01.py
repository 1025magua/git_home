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
import pytest

"""
1.主流程
"""


class TestLogin:
    cases = ReadExcel.read_data_pl(DATA_FILE, '登录', 1, 1)

    @pytest.mark.parametrize('case', cases)
    def test_login(self, case):
        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()

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
    pytest.main(["-vs", "./test_login01.py"])
