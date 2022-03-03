import pytest
import os

if __name__ == '__main__':
    pytest.main(
        ['-vs', './testcases/test_business_token_login02/test_login05.py', './testcases/test_my_interface01',
         '--alluredir=report/allure_json'])
    os.system('allure generate report/allure_json -o report/allure_report --clean')
