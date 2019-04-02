# coding=utf-8
import logging
import os

__author__ = 'TienHN'
_logger = logging.getLogger(__name__)


class DatabaseConfig:
    TK_RESULT_DB_HOST = os.getenv('TK_RESULT_DB_HOST', '123.31.32.171')
    TK_RESULT_DB_PORT = os.getenv('TK_RESULT_DB_PORT', '3306')
    TK_RESULT_DB_USER = os.getenv('TK_RESULT_DB_USER', 'bigdata')
    TK_RESULT_DB_PASS = os.getenv('TK_RESULT_DB_PASS', 'bigdata123')
    TK_RESULT_DB_NAME = os.getenv('TK_RESULT_DB_NAME', 'tk_result')

    CATALOG_DB_HOST = os.getenv('CATALOG_DB_HOST', '123.31.32.181')
    CATALOG_DB_PORT = os.getenv('CATALOG_DB_PORT', '3306')
    CATALOG_DB_USER = os.getenv('CATALOG_DB_USER', 'congtm')
    CATALOG_DB_PASS = os.getenv('CATALOG_DB_PASS', 'DgKoL3103b')
    CATALOG_DB_NAME = os.getenv('CATALOG_DB_NAME', 'catalog-live')

