#  F1 Telemetry Pipeline

An end-to-end Formula 1 telemetry ingestion, storage, and visualization pipeline. Designed to pull real-world F1 session data, store lap and sector metrics in PostgreSQL, and compare driver performance (such as Max Verstappen vs. Charles Leclerc) through interactive charts.

---

##  Tech Stack

- **Backend:** Python, Flask
- **Data & Telemetry:** FastF1
- **Database:** PostgreSQL
- **Frontend & Visualization:** HTML/CSS, JavaScript, Chart.js
- **Containerization:** Docker & Docker Compose

---

##  Prerequisites

Ensure you have the following installed on your local machine:
- Docker & Docker Compose
- Python 3.10+ (if running locally outside of containers)
- Git

---

##  Getting Started

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/AndileKwaziMsomi/f1-telemetry-pipeline.git](https://github.com/AndileKwaziMsomi/f1-telemetry-pipeline.git)
   cd f1-telemetry-pipeline
   ```

2. **Configure environment variables:**
   Create a `.env` file in the root directory with your database credentials:
   ```env
   DB_HOST=db
   DB_PORT=5432
   DB_NAME=f1_telemetry
   DB_USER=postgres
   DB_PASS=your_password
   ```

3. **Spin up with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Access the Dashboard:**
   Open your browser and navigate to `http://localhost:5000`.

---

##  Project Structure

```text
f1-telemetry-pipeline/
├── app/
│   ├── static/         # CSS, Chart.js scripts, and assets
│   ├── templates/      # HTML Jinja2 templates
│   ├── ingestion.py    # FastF1 data extraction and ETL pipeline
│   ├── models.py       # PostgreSQL database models
│   └── routes.py       # Flask API and dashboard routes
├── cache/              # FastF1 local session cache
├── docker-compose.yml  # Multi-container orchestration
├── Dockerfile          # Python application image
├── requirements.txt    # Python dependencies
└── README.md
```

---

##  Key Features

- **Automated Telemetry ETL:** Fetches official timing, speed, throttle, brake, and sector data via FastF1.
- **Persistent Storage:** Structures and stores session and lap records in PostgreSQL for fast querying.
- **Head-to-Head Comparisons:** Visualizes lap time deltas and telemetry traces between drivers across circuits.

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
