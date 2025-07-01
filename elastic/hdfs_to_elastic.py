import subprocess
import os
from elasticsearch import Elasticsearch

# Colores ANSI (azules)
class bcolors:
    HEADER = '\033[95m'
    BLUE = '\033[94m' 
    CYAN = '\033[96m'
    OKBLUE = '\033[34m'
    ENDC = '\033[0m'

ES_HOST = os.getenv("ELASTIC_HOST", "https://es01:9200")
ES_USER = os.getenv("ELASTIC_USER", "elastic")
ES_PASS = os.getenv("ELASTIC_PASSWORD", "changeme")

es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USER, ES_PASS),
    verify_certs=False
)

# Mapeo: índice destino -> archivo HDFS origen
hdfs_paths = {
    "analysis_by_city": "/user/hadoop/analysis_by_city/part-r-00000",
    "analysis_by_type": "/user/hadoop/analysis_by_type/part-r-00000",
    "analysis_by_type_city": "/user/hadoop/analysis_by_type_city/part-r-00000",
    "analysis_by_street_city": "/user/hadoop/analysis_by_street_city/part-r-00000",
    "analysis_by_day": "/user/hadoop/analysis_by_day/part-r-00000"
}

for index_name, hdfs_path in hdfs_paths.items():
    try:
        print(f"{bcolors.CYAN}→ Extrayendo datos desde HDFS: {hdfs_path}{bcolors.ENDC}")
        result = subprocess.run(
            ["/opt/hadoop/bin/hdfs", "dfs", "-cat", hdfs_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )

        for i, line in enumerate(result.stdout.strip().splitlines()):
            fields = line.split(",")
            es.index(index=f"clean_alerts_{index_name}", id=f"{index_name}-{i}", document={"fields": fields})

        print(f"{bcolors.OKBLUE}✔ Índice creado: clean_alerts_{index_name} ({i+1} documentos){bcolors.ENDC}\n")

    except subprocess.CalledProcessError as e:
        print(f"{bcolors.HEADER}✘ Error al leer {hdfs_path}:{bcolors.ENDC} {e.stderr.strip()}")
