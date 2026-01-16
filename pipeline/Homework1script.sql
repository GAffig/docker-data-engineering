-- There are 989009 trips in Noc 2025 with trip distance <= 1
SELECT COUNT(*)
FROM public.yellow_taxi_trips_2025_11
WHERE trip_distance <= 1;


-- 2025-11-21 is the pick up day with the longest trip distance of 99.81
SELECT DATE(tpep_pickup_datetime) as pickup_day, MAX(trip_distance) as max_distance 
FROM yellow_taxi_trips_2025_11 
WHERE trip_distance < 100 
GROUP BY DATE(tpep_pickup_datetime) 
ORDER BY max_distance DESC 
LIMIT 1;


-- zone 132 (JFK airport)
SELECT "PULocationID",SUM(total_amount) as total_amount_sum
FROM yellow_taxi_trips_2025_11
WHERE DATE(tpep_pickup_datetime) = '2025-11-18'
GROUP BY "PULocationID"
ORDER BY total_amount_sum DESC
LIMIT 1;


-- largest tip of 50 happen to be from passenger dropped off in the same zone "East Harlem North" or 74 
SELECT "DOLocationID",tip_amount
FROM yellow_taxi_trips_2025_11
WHERE "PULocationID" = 74
ORDER BY tip_amount DESC
LIMIT 1;



