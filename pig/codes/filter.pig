-- 1. Carga de datos originales desde HDFS (/data/waze_data.csv)
raw_data = LOAD '/data/waze_data.csv'
    USING PigStorage(',')
    AS (
        uuid:chararray,
        type:chararray,
        city:chararray,
        street:chararray,
        speed:chararray,
        reliability:chararray,
        confidence:chararray,
        country:chararray,
        reportRating:chararray,
        pubMillis:chararray,
        additionalInfo:chararray,
        fromNodeId:chararray,
        id:chararray,
        inscale:chararray,
        magvar:chararray,
        nComments:chararray,
        nThumbsUp:chararray,
        nearBy:chararray,
        provider:chararray,
        providerId:chararray,
        reportBy:chararray,
        reportByMunicipalityUser:chararray,
        reportDescription:chararray,
        reportMood:chararray,
        roadType:chararray,
        subtype:chararray,
        toNodeId:chararray
    );

-- 2. Eliminar duplicados exactos
deduped = DISTINCT raw_data;

-- 3. Filtrar registros válidos con campos clave no nulos y no vacíos
clean_data = FILTER deduped BY 
    (uuid IS NOT NULL AND TRIM(uuid) != '' AND
     type IS NOT NULL AND TRIM(type) != '' AND
     city IS NOT NULL AND TRIM(city) != '' AND
     street IS NOT NULL AND TRIM(street) != '' AND
     pubMillis IS NOT NULL AND TRIM(pubMillis) != '');

-- 4. Normalización y casting
homogenized = FOREACH clean_data GENERATE
    uuid,
    UPPER(TRIM(type)) AS type,
    UPPER(TRIM(city)) AS city,
    UPPER(TRIM(street)) AS street,
    (long)pubMillis AS timestamp;

-- 5. (Opcional) Agrupación y estadísticas básicas (si la necesitas)
grouped = GROUP homogenized BY (type, city);

unified = FOREACH grouped GENERATE
    FLATTEN(group) AS (type, city),
    COUNT(homogenized) AS count,
    MIN(homogenized.timestamp) AS first_timestamp,
    MAX(homogenized.timestamp) AS last_timestamp;

-- 6. Guardar los datos limpios y normalizados para el siguiente script
STORE homogenized INTO 'cleaned_records' USING PigStorage(',');
