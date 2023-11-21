import logging

# logging.warning('Watch out!')  # will print a message to the console
# logging.info('I told you so')  # will not print anything

# log level 从低到高
# DEBUG
# INFO
# WARNING
# ERROR

# logging.basicConfig(filename= 'example.log', level=logging.INFO, format='%(asctime)s %(message)s')

# logging.info('info message')
# logging.warning('warning message')
# logging.error('error message')

# 通过logger 对象来配置日志，既可以输出到控制台，也可以输出到文件
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
fh = logging.FileHandler('example.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(ch)
logger.addHandler(fh)

logger.info('info message')