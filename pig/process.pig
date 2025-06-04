-- Load the CSV data
raw_data = LOAD '/data/waze_alerts.csv' USING PigStorage(',') AS (
    reportBy:chararray,
    country:chararray,
    inscale:chararray,
    city:chararray,
    reportRating:int,
    reportByMunicipalityUser:chararray,
    confidence:int,
    reliability:int,
    type:chararray,
    fromNodeId:long,
    uuid:chararray,
    speed:int,
    reportMood:int,
    roadType:int,
    magvar:int,
    subtype:chararray,
    street:chararray,
    additionalInfo:chararray,
    wazeData:chararray,
    toNodeId:long,
    location_x:double,
    location_y:double,
    id:chararray,
    pubMillis:chararray
);

-- Filter unique alerts based on uuid
unique_alerts = DISTINCT raw_data;

-- Group by alert type
alerts_by_type = GROUP unique_alerts BY type;

-- Count alerts by type
count_by_type = FOREACH alerts_by_type GENERATE group AS alert_type, COUNT(unique_alerts) AS count;

-- Store results
STORE count_by_type INTO '/output/alerts_by_type';
STORE unique_alerts INTO '/output/unique_alerts';