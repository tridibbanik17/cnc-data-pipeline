# CNC Data Pipeline — Industry 4.0 Analytics Platform

> An end-to-end data pipeline for extracting, processing, analyzing, and visualizing real-time and historical CNC machine data to support manufacturing decision-making through dashboards, predictive analytics, and machine learning-driven insights.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Tech Stack](#tech-stack)
- [Data Model](#data-model)
- [Machine Learning Applications](#machine-learning-applications)
- [Dashboard Features](#dashboard-features)
- [Setup Instructions](#setup-instructions)
- [Project Goals](#project-goals)
- [Future Improvements](#future-improvements)
- [Author](#author)
- [License](#license)

---

## Overview

This project simulates a production-ready architecture for integrating CNC machine controller data (Fanuc, Haas, Heidenhain, Mitsubishi, etc.) into a centralized analytics platform for monitoring **OEE, cycle time, spindle load, tool wear, uptime/downtime, and alarms**.

The system is fully containerized via Docker Compose, with three independently running services — a Python simulator, a Flask backend, and a React frontend — orchestrated together with a single command.

It is intended to showcase skills relevant to smart manufacturing, data engineering, and industrial AI applications.

---

## Key Features

- Real-time and historical CNC machine data ingestion
- Scalable data pipeline for manufacturing metrics
- **KPI Tracking:**
  - Cycle time analysis
  - Machine uptime/downtime
  - Spindle load monitoring
  - Tool wear estimation
  - Alarm/event tracking
- Web-based dashboard for visualization
- Database-backed storage for structured machine data
- Data cleaning and preprocessing pipeline
- JWT-based authentication with role-based access control
- **Machine Learning Components:**
  - Anomaly detection via scikit-learn IsolationForest
  - Predictive maintenance
  - Performance trend analysis
- API layer for system integration
- Modular architecture for scalability

---

## System Architecture

![CNC Data Pipeline Architecture](docs/cnc_data_pipeline.svg)

*Click [here](docs/cnc_data_pipeline.svg) to view full size.*

---

## Tech Stack

| Category | Technologies |
|---|---|
| **Backend** | Python 3.11, Flask, Flask-CORS, psycopg2 |
| **Frontend** | React.js, Vite, Axios, Recharts |
| **Machine Learning** | Scikit-learn (IsolationForest), NumPy |
| **Database** | PostgreSQL |
| **Authentication** | PyJWT, Werkzeug (password hashing) |
| **Data & Integration** | REST APIs, OPC-UA / MTConnect (conceptual), Simulated CNC data streams |
| **Dev Tools** | Git / GitHub, Docker, Docker Compose, Makefile |

---

## Data Model

**Machine Data Table**

| Field | Description |
|---|---|
| `machine_id` | Unique identifier for the CNC machine |
| `timestamp` | Time of the recorded data point |
| `spindle_load` | Current spindle load value |
| `tool_wear` | Estimated tool wear level |
| `cycle_time` | Time taken per production cycle |
| `uptime` | Machine active time |
| `downtime` | Machine inactive time |
| `alarm_code` | Active alarm or event code |

---

## Machine Learning Applications

| Application | Description |
|---|---|
| **Anomaly Detection** | scikit-learn IsolationForest scores incoming telemetry and flags abnormal machine behaviour in real time at the ingest layer |
| **Predictive Maintenance** | Forecasting tool wear and failure probability from historical telemetry trends |
| **Performance Optimization** | Analyzing cycle time inefficiencies across machines |
| **Trend Analysis** | Long-term production performance insights via history API |

---

## Dashboard Features

- Real-time machine status monitoring
- OEE (Overall Equipment Effectiveness) visualization
- Cycle time trend charts (Recharts LineChart)
- Tool wear progression graphs
- Alarm history logs
- Downtime state tracking
- Admin panel for machine and user management (role-restricted)
- Multi-machine comparison view

---

## Setup Instructions

### 1. Clone the repository
```cmd
git clone https://github.com/tridibbanik17/cnc-data-pipeline.git
cd cnc-data-pipeline
```

### 2. Install dependencies
```cmd
cd .\backend
pip install -r requirements.txt
cd ..\simulator
pip install -r requirements.txt
cd ..
```

### 3. Configure database

Set the database connection string for the backend.  
If you're running the project using Docker Compose, use the internal Postgres URL in `.env` file inside the `backend` folder:
```cmd
cd .\backend
```

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/cnc_pipeline
```

If you're running the backend outside Docker, replace `db` with `localhost`:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/cnc_pipeline
```

### 4. Run backend server
```cmd
cd ..
docker builder prune -a
docker system prune -af
docker compose down --volumes --remove-orphans
docker compose build --no-cache
docker compose up
```

### 5. Launch frontend
Please open your internet browser and insert this URL in the top search box: `http://localhost:5173/`

---

## Project Goals

This project was developed to demonstrate practical experience in:

- Industrial data acquisition from CNC systems
- Real-time data pipeline design
- Manufacturing analytics and KPI tracking
- Web-based visualization dashboards
- Machine learning applications in anomaly detection and predictive maintenance
- JWT authentication and role-based access control
- Full-stack industrial software development
- Docker containerization and service orchestration

---

## Future Improvements

- Integration with real CNC controllers via OPC-UA / MTConnect
- Deployment on cloud platforms (AWS / Azure)
- Real-time streaming using Kafka or MQTT
- Advanced deep learning models for predictive failure detection
- Mobile dashboard support
- Grafana or Power BI integration for enhanced visualization

---

## Author

**Tridib Banik**  
Software Engineering Student — McMaster University  
Focused on Data Engineering, AI/ML, and Industrial Systems

---

## License

This project is for educational and portfolio purposes.