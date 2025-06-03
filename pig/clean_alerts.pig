-- clean_alerts.pig
REGISTER '/opt/pig/lib/json-simple-1.1.1.jar';

raw = LOAD 'input/alerts.json' USING JsonLoader('uuid:chararray, type:chararray, location:map[], street:chararray, city:chararray, country:chararray, pubMillis:long, description:chararray');

filtered = FILTER raw BY type IS NOT NULL AND location#x IS NOT NULL AND location#y IS NOT NULL;

unique = DISTINCT filtered;

with_time = FOREACH unique GENERATE 
    uuid, 
    type, 
    location#x AS lon:double, 
    location#y AS lat:double, 
    UDF_TO_DATETIME(pubMillis) AS ts, 
    LOWER(description) AS desc,
    city;

grouped = GROUP with_time BY (city, type);

summary = FOREACH grouped GENERATE 
    group.city AS comuna,
    group.type AS tipo,
    COUNT(with_time) AS total;

STORE summary INTO 'output/summary_cleaned' USING PigStorage(',');
