#-*-coding:utf-8-*-

from oslo_config import cfg
from oslo_log import log as logging
from os.path import join, dirname
from os import environ
import pymysql

# 创建对象CONF，用来充当容器
conf = cfg.CONF
log = logging.getLogger(__name__)
logging.register_options(conf)

# common
default_opts = [
    # cfg.StrOpt(name="debug", default=True),
    cfg.IntOpt(name="port", default=8888),
    cfg.StrOpt(name="env", default="debug"),  # 环境变量值
    cfg.StrOpt(name="environ", default="UNITYMOB_ENVIRON"),  # 环境变量key
]
# 注册含有多个配置项的模式
conf.register_opts(default_opts)
conf.register_cli_opts([
    cfg.IntOpt(name='port', default=8888),
])

# sqlalchemy
sqlalchemy = cfg.OptGroup(name='sqlalchemy', title="MySQL ORM 相关配置")
# 配置组必须在其组件被注册前注册
conf.register_group(sqlalchemy)
conf.register_cli_opts([
    cfg.BoolOpt('echo', default=True),
    cfg.BoolOpt('autoflush', default=True),
    cfg.IntOpt('pool_size', 10),
    cfg.IntOpt('pool_recycle', 3600)

], sqlalchemy)

pymysql.install_as_MySQLdb()

# mysql
mysql = cfg.OptGroup(name='mysql', title="MySQL DSN配置")
# 配置组必须在其组件被注册前注册
conf.register_group(mysql)
conf.register_cli_opts([
    cfg.StrOpt('unitymob', default='localhost'),
], mysql)

# redis
redis = cfg.OptGroup(name='redis', title="Redis 相关配置")
# 配置组必须在其组件被注册前注册
conf.register_group(redis)
conf.register_cli_opts([
    cfg.StrOpt('host', default='127.0.0.1'),
    cfg.IntOpt('port', default=6379),
    cfg.StrOpt('password', default='unitymob'),
    cfg.StrOpt('prefix', default='unitymob_'),
], redis)

# rabbitmq
rabbitmq = cfg.OptGroup(name='rabbitmq', title="Rabbitmq 相关配置")
# 配置组必须在其组件被注册前注册
conf.register_group(rabbitmq)
conf.register_cli_opts([
    cfg.StrOpt('dsn', default=''),
], rabbitmq)

env = environ.get(conf.environ, 'conf')
env = env if env in ['debug', 'pre', 'conf'] else 'conf'
conf(default_config_files=[join(dirname(__file__), '.'.join([env, 'ini']))])

logging.setup(conf, "unitymob")


if __name__ == '__main__':
    # 调用容器对象，传入要解析的文件（可以多个）
    cfg.CONF(default_config_files=['conf.ini'])
    print(cfg.CONF['rabbitmq']['dsn'])
    for i in cfg.CONF.rabbitmq:
        print(i)
