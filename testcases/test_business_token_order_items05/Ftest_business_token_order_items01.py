"""
-------------------------------------------------
   File Name:test_business_token_order_items01
   Author:Lee
   date: 2021/10/6-15:35
-------------------------------------------------
"""
import unittest, requests
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from ddt import ddt, data
from comms.db_utils import DBUtils
from comms.public_api import replace_data, get_token
from comms.log_utils import logger

"""
1.主流程
"""


@ddt
class TestOrderItems(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DBUtils()

    cases = ReadExcel.read_data_pl(DATA_FILE, 'business_token_order_items', 1, 1)

    @data(*cases)
    def test_orderItems(self, case):
        one = self.db.find_one('select * from tb_order order by rand();')
        orderId = one[0]

        if '#token#' in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
        if "#orderId#" in case.case_data:
            case.case_data = replace_data(case.case_data, 'orderId', orderId)

        response = requests.post(url=case.url, data=eval(case.case_data))
        res_body = response.json()

        try:
            # 四表连接查询orderId数据,如果查询多条和goods_tiems作比较,如果查询到数据，判断报文包含查询成功，如果没查到数据，判断报文包含查询无结果
            if case.case_id == 1:
                sql = 'select * from tb_user u,tb_order o,tb_goods g,tb_order_goods og where u.userId = o.userId ' \
                      'and o.orderId = og.orderId and og.goodsId = g.goodsId and o.orderId = %s;'
                count = self.db.find_count(sql, (orderId,))
                if count > 0:
                    self.assertEqual(count, len(res_body['goods_tiems']))
                    self.assertIn('查询成功', str(res_body))
                elif count == 0:
                    self.assertIn('查询无结果', str(res_body))
            else:
                self.assertEqual(eval(case.expect), res_body)
        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_order_items', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res_body))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_order_items', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
