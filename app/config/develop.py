"""
# @Author  wk
# @Time 2020/4/22 10:41

"""
from .default import Config


class DevelopConfig(Config):
    DEBUG = True
    LOG_LEVEl = "DEBUG"
