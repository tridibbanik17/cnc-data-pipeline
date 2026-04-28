CREATE TABLE IF NOT EXISTS machine_data (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    spindle_load FLOAT NOT NULL,
    tool_wear FLOAT NOT NULL,
    cycle_time FLOAT NOT NULL,
    uptime BOOLEAN NOT NULL,
    alarm_active BOOLEAN NOT NULL,
    alarm_code VARCHAR(50)
);

CREATE INDEX IF NOT EXISTS idx_machine_time
ON machine_data(machine_id, timestamp);

CREATE TABLE IF NOT EXISTS anomaly_flags (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    anomaly_type VARCHAR(50) NOT NULL,
    severity FLOAT NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'operator'
);