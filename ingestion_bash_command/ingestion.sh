#!/usr/bin/env bash
crontab -l | { cat; echo "*/1 * * * * /home/tienhn//IdeaProjects/product_listing_ingestion/ingestion_bash_command/ingest_catalog.sh /home/tienhn//IdeaProjects/product_listing_ingestion >> /home/tienhn//IdeaProjects/product_listing_ingestion/var/log/ingestion.log 2>&1"; } | crontab -