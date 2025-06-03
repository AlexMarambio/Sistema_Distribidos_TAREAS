#!/bin/bash

# Asumiendo que tienes Hadoop y Pig instalados
hadoop fs -mkdir -p input
hadoop fs -put alerts.json input/

pig clean_alerts.pig

hadoop fs -get output/summary_cleaned summary.csv

set -e

echo "🔄 Exportando alertas desde Elasticsearch a pig/alerts.json..."
python3 ../tools/export_alerts.py

echo "📂 Creando carpeta input en HDFS (si no existe)..."
hadoop fs -mkdir -p input || true

echo "📤 Subiendo archivo alerts.json a HDFS..."
hadoop fs -put -f alerts.json input/

echo "🐷 Ejecutando script de limpieza y homogeneización en Apache Pig..."
pig clean_alerts.pig

echo "📥 Descargando resultados desde HDFS a pig/summary.csv..."
hadoop fs -get -f output/summary_cleaned summary.csv

echo "✅ Proceso completo. Resultado en pig/summary.csv"