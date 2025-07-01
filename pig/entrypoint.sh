#!/bin/bash

# Configuración de las env
HADOOP_HOME=/opt/hadoop
PIG_HOME=/opt/pig
DATA_DIR=/data
HDFS_INPUT=/data
HDFS_OUTPUT=/output
PIG_SCRIPT=/codes/filter.pig
PIG_SCRIPT2=/codes/process.pig
CSV_FILE=waze_data.csv
HDFS_FILE=waze_data.csv

# Iniciar servicios SSH y Hadoop
echo "Preparando entorno..."
echo "Iniciando servicio SSH..."
sudo service ssh start

echo "Verificando si es necesario formatear NameNode..."
if [ ! -d "$HADOOP_HOME/data/namenode/current" ]; then
    $HADOOP_HOME/bin/hdfs namenode -format -force
fi

ssh-keyscan -H localhost >> ~/.ssh/known_hosts 2>/dev/null
ssh-keyscan -H 0.0.0.0 >> ~/.ssh/known_hosts 2>/dev/null

echo "Iniciando HDFS (start-dfs.sh)..."
$HADOOP_HOME/sbin/start-dfs.sh

echo "Iniciando YARN (start-yarn.sh)..."
$HADOOP_HOME/sbin/start-yarn.sh

echo "⏳ Esperando a que HDFS termine de inicializarse..."
sleep 10

# Configurar estructura HDFS
echo "📁 Configurando directorios de entrada y salida en HDFS..."
$HADOOP_HOME/bin/hdfs dfs -mkdir -p $HDFS_INPUT
$HADOOP_HOME/bin/hdfs dfs -mkdir -p $HDFS_OUTPUT
$HADOOP_HOME/bin/hdfs dfs -chmod -R 755 $HDFS_INPUT
$HADOOP_HOME/bin/hdfs dfs -chmod -R 755 $HDFS_OUTPUT

# Esperar y verificar archivo CSV
echo "📄 Esperando disponibilidad del archivo CSV en $DATA_DIR..."
while [ ! -f "$DATA_DIR/$CSV_FILE" ]; do
    echo "🔄 Esperando que $CSV_FILE aparezca..."
    sleep 15
done

# Subir archivo a HDFS con reintentos
MAX_RETRIES=3
RETRY_COUNT=0
UPLOAD_SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$UPLOAD_SUCCESS" = false ]; do
    echo "🚚 Subiendo archivo a HDFS (Intento $((RETRY_COUNT+1)) de $MAX_RETRIES)..."

    $HADOOP_HOME/bin/hdfs dfs -put -f $DATA_DIR/$CSV_FILE $HDFS_INPUT/$HDFS_FILE

    if [ $? -eq 0 ]; then
        HDFS_SIZE=$($HADOOP_HOME/bin/hdfs dfs -du -s $HDFS_INPUT/$HDFS_FILE | awk '{print $1}')
        LOCAL_SIZE=$(du -b $DATA_DIR/$CSV_FILE | awk '{print $1}')

        if [ "$HDFS_SIZE" -eq "$LOCAL_SIZE" ]; then
            echo "✅ Subida exitosa: $HDFS_SIZE bytes verificados"
            UPLOAD_SUCCESS=true
        else
            echo "⚠️  Tamaños distintos detectados (HDFS: $HDFS_SIZE vs Local: $LOCAL_SIZE)"
        fi
    else
        echo "❌ Falló el intento $((RETRY_COUNT+1)) de subida"
    fi

    RETRY_COUNT=$((RETRY_COUNT+1))
    sleep 5
done

if [ "$UPLOAD_SUCCESS" = false ]; then
    echo "🛑 Error: No se pudo subir el archivo tras $MAX_RETRIES intentos"
    exit 1
fi

# Configurar entorno Pig y rutas
export PIG_CLASSPATH=$HADOOP_HOME/etc/hadoop:$HADOOP_HOME/share/hadoop/common/*:$HADOOP_HOME/share/hadoop/mapreduce/*:$HADOOP_HOME/share/hadoop/hdfs/*:$HADOOP_HOME/share/hadoop/yarn/*

# Esperar que YARN esté disponible
echo "Esperando disponibilidad de YARN..."
until $HADOOP_HOME/bin/yarn node -list 2>/dev/null | grep -q "RUNNING"; do
    sleep 5
done

echo "Verificando presencia del archivo en HDFS:"
$HADOOP_HOME/bin/hdfs dfs -ls $HDFS_INPUT/$HDFS_FILE

echo "Iniciando JobHistory Server..."
$HADOOP_HOME/sbin/mr-jobhistory-daemon.sh start historyserver

# Ejecutar scripts Pig
echo "🐷 Ejecutando script Pig de filtrado (filter.pig)..."
$PIG_HOME/bin/pig -f $PIG_SCRIPT

echo "🐷 Ejecutando script Pig de análisis (process.pig)..."
sleep 5
$PIG_HOME/bin/pig -f $PIG_SCRIPT2

echo "📁 Verificando que se haya generado /output/analysis_by_type..."
if $HADOOP_HOME/bin/hdfs dfs -test -e /user/hadoop/cleaned_records; then
    echo "✅ Análisis por tipo generado correctamente."
else
    echo "❌ No se generó /user/hadoop/cleaned_records. Revisa que los nombres de campos estén alineados entre scripts."
fi


## Colores
GREEN="\033[0;32m"
LIGHT_GREEN="\033[1;32m"
CYAN="\033[0;36m"
RESET="\033[0m"

# Mostrar resultados
echo -e "${LIGHT_GREEN}==== Mostrando resultados de salida Pig ====${RESET}"

echo -e "${GREEN}- Registros limpios:${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/cleaned_records/part-r-00000
sleep 5

echo -e "${GREEN}- Análisis por comuna:${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/analysis_by_city/part-r-00000
sleep 5

echo -e "${GREEN}- Análisis por día (formato epoch):${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/analysis_by_day/part-r-00000
sleep 5

echo -e "${GREEN}- Análisis por calle y comuna:${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/analysis_by_street_city/part-r-00000
sleep 5

echo -e "${GREEN}- Análisis por tipo de alerta:${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/analysis_by_type/part-r-00000
sleep 5

echo -e "${GREEN}- Análisis por tipo de alerta y comuna:${RESET}"
$HADOOP_HOME/bin/hdfs dfs -cat /user/hadoop/analysis_by_type_city/part-r-00000
sleep 5


echo "📥 Descargando resultados a ./data local..."

mkdir -p $DATA_DIR
mkdir -p $DATA_DIR/output


$HADOOP_HOME/bin/hdfs dfs -get -f /user/hadoop/analysis_by_city $DATA_DIR/output/
$HADOOP_HOME/bin/hdfs dfs -get -f /user/hadoop/analysis_by_type $DATA_DIR/output/
$HADOOP_HOME/bin/hdfs dfs -get -f /user/hadoop/analysis_by_type_city $DATA_DIR/output/
$HADOOP_HOME/bin/hdfs dfs -get -f /user/hadoop/analysis_by_street_city $DATA_DIR/output/
$HADOOP_HOME/bin/hdfs dfs -get -f /user/hadoop/analysis_by_day $DATA_DIR/output/

# Mantener contenedor activo
echo "✅ Todos los procesos finalizados exitosamente. El contenedor permanece activo para revisión."
tail -f /dev/null
