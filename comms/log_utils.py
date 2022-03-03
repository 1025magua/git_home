"""
-------------------------------------------------
   File Name:log_utils
   Author:Lee
   date: 2021/9/27-11:49
-------------------------------------------------
"""

# 第一步:导入logging
import logging
from comms.constants import INFO_FILE, ERROR_FILE


def get_logger():
    # 第二步:创建日志对象
    logger = logging.getLogger('logging')
    logger.setLevel("DEBUG")  # 设置默认的日志级别DEBUG，代表获取DEBUG及DEBUG以上级别的日志

    # 第三步:设置输出方向

    # 输出到控制台，并且级别INFO，代表INFO及INFO以上级别的内容
    sh1 = logging.StreamHandler()
    sh1.setLevel('INFO')  # 输出INFO及INFO级别以上的内容

    # 输出到 ./info.log 文件,并且内容为追加写入,级别是INFO及INFO级别以上的内容
    sh2 = logging.FileHandler(filename=INFO_FILE, mode='a', encoding='utf-8')
    sh2.setLevel('INFO')

    # 输出到 ./error.log 文件,并且内容为追加写入,级别是ERROR及ERROR级别以上的内容
    sh3 = logging.FileHandler(filename=ERROR_FILE, mode='a', encoding='utf-8')
    sh3.setLevel('ERROR')

    # 第四步:添加输出方向到logger对象
    logger.addHandler(sh1)
    logger.addHandler(sh2)
    logger.addHandler(sh3)

    # 第五步:指定日志输出格式
    fmt_str = '%(asctime)s - [%(filename)s - line:%(lineno)d] - %(levelname)s:%(message)s'
    my_fmt = logging.Formatter(fmt_str)  # 设置样式
    sh1.setFormatter(my_fmt)
    sh2.setFormatter(my_fmt)
    sh3.setFormatter(my_fmt)

    return logger


logger = get_logger()
