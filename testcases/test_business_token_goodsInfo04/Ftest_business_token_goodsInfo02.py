"""
-------------------------------------------------
   File Name:test_business_token_goodsInfo01
   Author:Lee
   date: 2021/10/5-17:33
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
"""


@ddt
class TestTokenGoodsInfo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DBUtils()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_token_goodsInfo', 1, 1)

    @data(*cases)
    def test_token_goods_info(self, case):

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()

        try:
            if case.case_id == 1:
                self.assertIn(case.expect, str(res_body))  # 判断响应体包含 查询成功
                # 判断查询商品条目数是否正确
                # 1.获取返回的结果的条目数
                res_count = len(res_body['goods_tiems'])
                db_count = self.db.find_count('select * from tb_goods;')
                self.assertEqual(res_count, db_count)  # 响应体的商品条目数和数据库的商品条目数做对比
            else:
                self.assertEqual(eval(case.expect), res_body)
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goodsInfo', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goodsInfo', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
