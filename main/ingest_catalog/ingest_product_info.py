# coding=utf-8
import logging
import logging.config

__author__ = 'TienHN'
logging.config.fileConfig("logging.ini")
_logger = logging.getLogger("ingest_catalog")

if __name__ == "__main__":
    _logger.info("Catalog")
    _logger.error("Catalog")
