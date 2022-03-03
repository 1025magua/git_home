import pytest
import os

if __name__ == '__main__':
    pytest.main(['-vs', './testcases/', '--alluredir=report/allure_json'])
    os.system('allure generate report/allure_json -o report/allure_report --clean')
