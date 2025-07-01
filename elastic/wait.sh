#!/bin/bash

# Colores
BLUE='\033[1;34m'
GREEN='\033[1;32m'
RESET='\033[0m'

echo -e "${BLUE}⏳ Esperando archivos procesados por Hadoop en /data/output/...${RESET}"
until [ -f "/data/output/analysis_by_day/part-r-00000" ]; do
    sleep 5
done

echo -e "${GREEN}✅ Archivos detectados. Ejecutando exportadores...${RESET}"

python elastic/mongo_to_elastic.py
#python elastic/hdfs_to_elastic.py
