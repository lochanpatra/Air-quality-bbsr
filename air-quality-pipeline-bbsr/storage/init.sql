
-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Create hypertable for air quality measurements
CREATE TABLE aq_stations (
  id SERIAL PRIMARY KEY,
  station_id TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  pm25 FLOAT NOT NULL,
  geom GEOMETRY(Point, 4326) NOT NULL
);

SELECT create_hypertable('aq_stations', 'timestamp', if_not_exists => TRUE);
