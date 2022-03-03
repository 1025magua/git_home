"""
-------------------------------------------------
   File Name:test_business_goods_delete01
   Author:Lee
   date: 2021/10/8-15:45
-------------------------------------------------
"""
import unittest, requests
from ddt import ddt, data
from comms.excel_utils import ReadExcel
from comms.constants import DATA_FILE
from comms.public_api import replace_data, get_token, get_ini_data
from comms.log_utils import logger
from comms.db_utils import DBUtils

"""
1.主流程
2.数据回滚和数据验证
3.追加其他案例
"""


@ddt
class TestGoodsDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = DBUtils()

    cases = ReadExcel.read_data_all(DATA_FILE, 'business_token_goods_delete')

    @data(*cases)
    def test_goods_delete(self, case):
        if "#token#" in case.case_data:
            case.case_data = replace_data(case.case_data, 'token', get_token())
        if '#goodsId#' in case.case_data:
            if case.case_id == 7:
                case.case_data = replace_data(case.case_data, 'goodsId', get_ini_data('goodsId1', 'goodsId'))
            else:
                case.case_data = replace_data(case.case_data, 'goodsId', get_ini_data('goodsId2', 'goodsId'))

        if case.case_id == 1:
            self.db.cud("INSERT INTO `businessdb`.`tb_goods` (`goodsId`, `goodsName`, `goodsTypeId`, `descp`, `num`,"
                        " `onTime`, `offTime`, `shopPrice`, `promotePrice`, `promoteStartTime`, `promoteEndTime`, "
                        "`isOnSale`, `isPromote`, `givePoints`) VALUES (%s, 'iPhone13', '10001', '没有改变世界', "
                        "'9999', '2021-08-31 10:52:19', '2099-12-31', '5999.00', '0.00', '2021-10-02', '2022-10-28',"
                        " '1', '0', '10');", (get_ini_data('goodsId2', 'goodsId'),))

        response = requests.post(url=case.url, data=eval(case.case_data))
        res = response.json()

        try:
            self.assertEqual(eval(case.expect), res)
            if case.case_id == 1:
                count = self.db.find_count('select * from tb_goods where goodsId = %s',
                                           (get_ini_data('goodsId2', 'goodsId'),))
                self.assertEqual(0, count)

        except AssertionError as e:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_delete', case.case_id, 7, '失败')
            logger.error('测试编号{},测试用例标题:{},执行失败,实际结果为:{}!'.format(case.case_id, case.case_title, res))
            logger.exception(e)
            raise e
        else:
            ReadExcel.write_data(DATA_FILE, 'business_token_goods_delete', case.case_id, 7, '成功')
            logger.info('测试编号{},测试用例标题:{},执行成功!'.format(case.case_id, case.case_title))

    @classmethod
    def tearDownClass(cls):
        cls.db.close()
