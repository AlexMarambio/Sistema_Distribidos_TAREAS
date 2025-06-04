#!/bin/bash

# Start SSH
service ssh start

# Format HDFS
hdfs namenode -format -force

# Start Hadoop services
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

# Wait for HDFS to be available
until hdfs dfsadmin -report 2>/dev/null; do
  echo "Waiting for HDFS to start..."
  sleep 5
done

# Create directories
hdfs dfs -mkdir -p /data
hdfs dfs -mkdir -p /output

# Copy data if exists
if [ -f /data/waze_alerts.csv ]; then
  hdfs dfs -put /data/waze_alerts.csv /data/
  echo "Data copied to HDFS"
fi

# Run Pig script
echo "Starting Pig processing..."
pig -x mapreduce -f /app/process.pig

# Keep container running
echo "Processing completed. Container keeps running..."
tail -f /dev/null