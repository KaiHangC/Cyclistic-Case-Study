USE cyclistic_database;

DROP TABLE IF EXISTS BikeRides;

CREATE TABLE BikeRides (
    ride_id VARCHAR(50) NOT NULL,
    rideable_type VARCHAR(20) NOT NULL,
    started_at DATETIME NOT NULL,
    ended_at DATETIME NOT NULL,
    start_station_name VARCHAR(100) NOT NULL,
    start_station_id VARCHAR(50) NOT NULL,
    end_station_name VARCHAR(100) NOT NULL,
    end_station_id VARCHAR(50) NOT NULL,
    start_lat DECIMAL(10, 8) NOT NULL,
    start_lng DECIMAL(11, 8) NOT NULL,
    end_lat DECIMAL(10, 8) NOT NULL,
    end_lng DECIMAL(11, 8) NOT NULL,
    member_casual VARCHAR(10) NOT NULL CHECK (member_casual IN ('member', 'casual')),
    ride_length TIME NOT NULL,
    day_of_week TINYINT NOT NULL CHECK (day_of_week BETWEEN 1 AND 7)
);
