USE cyclistic_database;

--average ride time by rider type
SELECT 
    member_casual, 
    CONVERT(TIME, DATEADD(SECOND, AVG(CAST(DATEDIFF(SECOND, '00:00:00', ride_length) AS BIGINT)), '00:00:00')) AS avg_ride_length
FROM BikeRides
GROUP BY member_casual;

--bike type by member and bike
SELECT 
    member_casual,
    rideable_type,
    COUNT(*) AS trip_count
FROM 
    BikeRides
GROUP BY 
    member_casual, rideable_type
ORDER BY 
    member_casual, rideable_type;

--the day of the week with total count by the ride type
SELECT 
    day_of_week,
    SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_rides,
    SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_rides,
    COUNT(*) AS total_rides
FROM 
    BikeRides
GROUP BY 
    day_of_week
ORDER BY 
    day_of_week;

--the month of the year with total count by the ride type
SELECT
    YEAR(started_at) AS ride_year,
    MONTH(started_at) AS ride_month,
    DATENAME(month, started_at) AS month_name, 
    SUM(CASE WHEN member_casual = 'member' THEN 1 ELSE 0 END) AS member_rides,
    SUM(CASE WHEN member_casual = 'casual' THEN 1 ELSE 0 END) AS casual_rides,
    COUNT(*) AS total_rides
FROM
    BikeRides
GROUP BY
    YEAR(started_at),
    MONTH(started_at),
    DATENAME(month, started_at)
ORDER BY
    ride_year,
    ride_month;

--count most used station by casual rider
SELECT TOP 10
	COUNT(start_station_name) AS total_trip,
	start_station_name
FROM 
	BikeRides
WHERE member_casual = 'casual'
GROUP BY start_station_name
ORDER BY total_trip DESC

SELECT TOP 10
	COUNT(end_station_name) AS total_trip,
	end_station_name
FROM 
	BikeRides
WHERE member_casual = 'casual'
GROUP BY end_station_name
ORDER BY total_trip DESC


