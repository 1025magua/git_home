"""
-------------------------------------------------
   File Name:test_business_goods_promote01
   Author:Lee
   date: 2021/10/8-10:26
-------------------------------------------------
"""
import unittest, requests
from ddt import ddt, data
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.public_api import replace_data, get_token, get_ini_data
from comms.db_utils import DBUtils
from comms.log_utils import logger

"""
1.主流程
2.数据回滚和数据验证
"""


@ddt
class TestGoodsPromote(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DBUtils()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_token_goods_promote', 1, 1)

    @data(*cases)
    def test_goods_promote(self, case):
        res = self.db.find_one(
            'select goodsId from tb_goods where isPromote = 1 and isOnSale = 0 and goodsId != %s order by rand()',
            (get_ini_data('goodsId1', 'goodsId'),))

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
        if '#goodsId#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'goodsId', res[0])

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()

        try:
            self.assertEqual(eval(case.expect), res_body)
            # 验证数据库，断言响应结果已更改完成
            count = self.db.find_count('select * from tb_goods where goodsId = %s and isPromote = 0', (res[0],))
            self.assertEqual(1, count)
            # 数据回滚，将数据还原
            self.db.cud('update tb_goods set isPromote = 1 where goodsId = %s', (res[0],))
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_promote', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_promote', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()