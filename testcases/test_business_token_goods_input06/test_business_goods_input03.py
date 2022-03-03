"""
-------------------------------------------------
   File Name:test_business_goods_input01
   Author:Lee
   date: 2021/10/7-9:44
-------------------------------------------------
"""

import unittest, requests
from ddt import ddt, data
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.log_utils import logger
from comms.public_api import replace_data, get_token
from comms.db_utils import DBUtils

"""
1.主流程
2.数据回滚和数据验证
3.追加其它用例
"""


@ddt
class TestGoodsInput(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DBUtils()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_goods_input')

    @data(*cases)
    def test_goods_input(self, case):

        if case.case_id in (1, 3, 10, 11, 14, 18, 25):
            self.db.cud('delete from tb_goods where goodsName = %s', (eval(case.case_data)["goodsName"],))

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()

        try:
            self.assertEqual(eval(case.expect), res)
            if case.case_id in (1, 3, 10, 11, 14, 18, 25):
                count = self.db.find_count('select * from tb_goods where goodsName = %s',
                                           (eval(case.case_data)["goodsName"],))
                self.assertEqual(1, count)

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_input', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_input', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
