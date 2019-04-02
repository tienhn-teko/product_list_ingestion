import logging

import numpy as np
import pandas as pd
from string import Template
from sqlalchemy import create_engine

from main.config import DatabaseConfig

__author__ = 'TienHN'
_logger = logging.getLogger("ingest_sales")


def collect_quantity_and_revenue_by_pv_sku():
    # join pv_sku voi tien va so luong hang ban ra
    pv_sku_df = _collect_product_sku()
    quan_reve_df = _collect_quantity_and_revenue()
    merged_products_df = pd.merge(
        pv_sku_df, quan_reve_df,
        on='pv_sku',
        how='left').fillna({'tien_ban_ra': 0, 'sl_ban_ra': 0})
    # lay gia tri max va min khac 0
    tien_ban_ra = np.asarray(
        merged_products_df.iloc[:]['tien_ban_ra'].values)
    sl_ban_ra = np.asarray(merged_products_df.iloc[:]['sl_ban_ra'].values)
    tien_ban_ra = tien_ban_ra[tien_ban_ra > 0]
    sl_ban_ra = sl_ban_ra[sl_ban_ra > 0]
    tien_ban_ra_min = min(tien_ban_ra, default=0)
    tien_ban_ra_max = max(tien_ban_ra, default=0)
    sl_ban_ra_min = min(sl_ban_ra, default=0)
    sl_ban_ra_max = max(sl_ban_ra, default=0)
    # normalize quantity va revenue
    normalized_df = merged_products_df
    normalized_df['revenue'] = normalized_df['tien_ban_ra'].apply(
        normalize_func(tien_ban_ra_min, tien_ban_ra_max))
    normalized_df['quantity'] = normalized_df['sl_ban_ra'].apply(
        normalize_func(sl_ban_ra_min, sl_ban_ra_max))
    normalized_df.drop(columns=['tien_ban_ra', 'sl_ban_ra'], inplace=True)
    normalized_df.rename(columns={'pv_sku': 'sku'}, inplace=True)
    return normalized_df.to_dict('records')


def _collect_product_sku():
    catalog_template = Template(
        'mysql+pymysql://$user:$password@$host:$port/$database'
    ).substitute(
        user=DatabaseConfig.CATALOG_DB_USER,
        password=DatabaseConfig.CATALOG_DB_PASS,
        host=DatabaseConfig.CATALOG_DB_HOST,
        port=DatabaseConfig.CATALOG_DB_PORT,
        database=DatabaseConfig.CATALOG_DB_NAME)
    engine = create_engine(catalog_template)
    pv_sku_df = pd.read_sql_table(
        table_name='products', con=engine, columns=['pv_sku'])
    return pv_sku_df


def _collect_quantity_and_revenue():
    tk_result_template = Template(
        'mysql+pymysql://$user:$password@$host:$port/$database'
    ).substitute(
        user=DatabaseConfig.TK_RESULT_DB_USER,
        password=DatabaseConfig.TK_RESULT_DB_PASS,
        host=DatabaseConfig.TK_RESULT_DB_HOST,
        port=DatabaseConfig.TK_RESULT_DB_PORT,
        database=DatabaseConfig.TK_RESULT_DB_NAME)
    engine = create_engine(tk_result_template)
    sql_query = _build_aggregate_sale_quantity_and_revenue_query()
    quan_reve_df = pd.read_sql(sql=sql_query, con=engine)
    quan_reve_df.rename(columns={'ma_vt': 'pv_sku'}, inplace=True)
    return quan_reve_df


def _build_aggregate_sale_quantity_and_revenue_query():
    return "SELECT " \
           "ma_vt, " \
           "sum(CASE WHEN ma_ct = 'PTX' THEN tien2 ELSE 0 END) " \
           "- sum(CASE WHEN ma_ct = 'HDF' THEN tien2 ELSE  0 END) as tien_ban_ra, " \
           "sum(CASE WHEN ma_ct = 'PTX' THEN  so_luong ELSE 0 END) " \
           "- sum(CASE WHEN ma_ct = 'HDF' THEN so_luong ELSE 0 END) as sl_ban_ra " \
           "FROM " \
           "daily_revenue_detail_v1 " \
           "WHERE " \
           "DATEDIFF(CURDATE(), ngay_ct) <= 30 " \
           "GROUP BY " \
           "ma_vt " \
           "ORDER BY " \
           "ma_vt "


def normalize_func(value_min, value_max):
    def normalize(x):
        return (x - value_min) / (value_max - value_min) if x > 0 else 0

    return normalize


def do_ingestion():
    raw_data = collect_quantity_and_revenue_by_pv_sku()
    resp = EsProductService.save_all(raw_data)


if __name__ == "__main__":
    do_ingestion()
