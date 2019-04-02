#!/usr/bin/env bash
cd /home/tienhn//IdeaProjects/product_listing_ingestion
source .venv/bin/activate
python3 main/ingest_catalog/ingest_product_info.py
deactivate