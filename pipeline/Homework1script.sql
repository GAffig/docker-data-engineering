-- There are 989009 trips in Noc 2025 with trip distance <= 1
SELECT COUNT(*)
FROM public.green_taxi_trips_2025_11
WHERE trip_distance <= 1;


-- 2025-11-14 is the pick up day with the longest trip distance of 88.03
SELECT DATE(lpep_pickup_datetime) as pickup_day, MAX(trip_distance) as max_distance 
FROM green_taxi_trips_2025_11 
WHERE trip_distance < 100 
GROUP BY DATE(lpep_pickup_datetime) 
ORDER BY max_distance DESC 
LIMIT 1;



-- zone 74 (East Harlem North) has the highest total amount of 9281.92 on 2025-11-18
SELECT "PULocationID",SUM(total_amount) as total_amount_sum
FROM green_taxi_trips_2025_11
WHERE DATE(tpep_pickup_datetime) = '2025-11-18'
GROUP BY "PULocationID"
ORDER BY total_amount_sum DESC
LIMIT 1;


-- largest tip of 81.89 happen to be from passenger dropped off in the Yorkville West Zone (DOLocationID = 263) when picked up from East Harlem North (PULocationID = 74) 
SELECT "DOLocationID",tip_amount
FROM green_taxi_trips_2025_11
WHERE "PULocationID" = 74
ORDER BY tip_amount DESC
LIMIT 1;



