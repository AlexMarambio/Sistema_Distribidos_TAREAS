# Imagen base con Ubuntu
FROM ubuntu:20.04

# Evitar preguntas interactivas al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instalación de dependencias necesarias
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget python3 python3-pip unzip && \
    apt-get clean

# Instalación de Hadoop (requisito de Pig)
RUN wget https://downloads.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz && \
    tar -xvzf hadoop-3.3.6.tar.gz -C /opt && \
    mv /opt/hadoop-3.3.6 /opt/hadoop && \
    rm hadoop-3.3.6.tar.gz

ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$HADOOP_HOME/bin:$PATH

# Instalación de Pig
RUN wget https://downloads.apache.org/pig/pig-0.17.0/pig-0.17.0.tar.gz && \
    tar -xvzf pig-0.17.0.tar.gz -C /opt && \
    mv /opt/pig-0.17.0 /opt/pig && \
    rm pig-0.17.0.tar.gz

ENV PIG_HOME=/opt/pig
ENV PATH=$PIG_HOME/bin:$PATH

# Añadir soporte para JSON en Pig
RUN wget https://repo1.maven.org/maven2/com/googlecode/json-simple/json-simple/1.1.1/json-simple-1.1.1.jar -P /opt/pig/lib/

# Instalar elasticsearch client para Python
RUN pip3 install elasticsearch

# Establecer PYTHONPATH para que reconozca el módulo storage
ENV PYTHONPATH=/storage

# Establecer el directorio de trabajo
WORKDIR /pig

# Copiar scripts Pig y archivo alerts.json (cuando esté generado)
COPY ../pig/ /pig/

# Copiar script Python
COPY ../tools/export_alerts.py /tools/export_alerts.py

# Copiar módulo Python de conexión a Elasticsearch
COPY ../storage /storage

# Comando por defecto (puedes personalizarlo según necesites)
CMD ["bash"]
