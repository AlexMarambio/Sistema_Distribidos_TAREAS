-- 1. Cargar datos limpios desde HDFS
raw_data = LOAD '/user/hadoop/cleaned_records'
    USING PigStorage(',')
    AS (
        uuid:chararray,
        type:chararray,
        city:chararray,
        street:chararray,
        timestamp:long
    );

-- 2. Total de incidentes por ciudad
by_city = GROUP raw_data BY city;
city_metrics = FOREACH by_city GENERATE
    group AS city,
    COUNT(raw_data) AS total_incidents;

STORE city_metrics INTO '/user/hadoop/analysis_by_city' USING PigStorage(',');

-- 3. Total de incidentes por tipo
by_type = GROUP raw_data BY type;
type_metrics = FOREACH by_type GENERATE
    group AS type,
    COUNT(raw_data) AS total_incidents;

STORE type_metrics INTO '/user/hadoop/analysis_by_type' USING PigStorage(',');

-- 4. Total de incidentes por tipo y ciudad
by_type_city = GROUP raw_data BY (type, city);
type_city_metrics = FOREACH by_type_city GENERATE
    FLATTEN(group) AS (type, city),
    COUNT(raw_data) AS total_incidents;

STORE type_city_metrics INTO '/user/hadoop/analysis_by_type_city' USING PigStorage(',');

-- 5. Total de incidentes por calle y ciudad
by_street_city = GROUP raw_data BY (street, city);
street_city_metrics = FOREACH by_street_city GENERATE
    FLATTEN(group) AS (street, city),
    COUNT(raw_data) AS total_incidents;

STORE street_city_metrics INTO '/user/hadoop/analysis_by_street_city' USING PigStorage(',');

-- 6. Total de incidentes por día (día en formato epoch basado en timestamp ms)
by_day = FOREACH raw_data GENERATE
    (long)(timestamp / 86400000) AS day_epoch,
    type,
    city;

group_by_day = GROUP by_day BY day_epoch;
day_metrics = FOREACH group_by_day GENERATE
    group AS day_epoch,
    COUNT(by_day) AS total_incidents;

STORE day_metrics INTO '/user/hadoop/analysis_by_day' USING PigStorage(',');
