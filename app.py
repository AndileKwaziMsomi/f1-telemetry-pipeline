import os
import time
from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import fastf1
import pandas as pd

app = Flask(__name__)

# Configure FastF1 Cache
if not os.path.exists('f1_cache'):
    os.makedirs('f1_cache')
fastf1.Cache.enable_cache('f1_cache')

# Database connection details
DB_USER = os.getenv('DB_USER', 'f1_admin')
DB_PASS = os.getenv('DB_PASS', 'formula1pass')
DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('DB_NAME', 'f1_telemetry')

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

def init_db():
    """Wait for PostgreSQL container and create table if not exists."""
    retries = 5
    while retries > 0:
        try:
            with engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS driver_laps (
                        id SERIAL PRIMARY KEY,
                        driver VARCHAR(5),
                        lap_number INT,
                        lap_time_sec FLOAT,
                        compound VARCHAR(20),
                        tyre_life INT
                    );
                """))
                conn.commit()
            print("Database initialized successfully!")
            break
        except Exception as e:
            print(f"Database connection waiting... ({e})")
            retries -= 1
            time.sleep(3)

@app.route('/')
def home():
    return "F1 Telemetry Service Active! Call /api/f1/fetch to sync session data."

@app.route('/api/f1/fetch')
def fetch_f1_data():
    """Fetch 2024 Jeddah Grand Prix race session data for VER and LEC."""
    session = fastf1.get_session(2024, 'Jeddah', 'R')
    session.load()

    laps = session.laps.pick_drivers(['VER', 'LEC'])

    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE driver_laps;"))

        for idx, lap in laps.iterlaps():
            lap_sec = lap['LapTime'].total_seconds() if not pd.isna(lap['LapTime']) else None
            if lap_sec:
                conn.execute(text("""
                    INSERT INTO driver_laps (driver, lap_number, lap_time_sec, compound, tyre_life)
                    VALUES (:driver, :lap_num, :lap_sec, :compound, :tyre_life);
                """), {
                    "driver": lap['Driver'],
                    "lap_num": int(lap['LapNumber']),
                    "lap_sec": float(lap_sec),
                    "compound": str(lap['Compound']),
                    "tyre_life": int(lap['TyreLife'])
                })
        conn.commit()

    return jsonify({"status": "success", "message": "Jeddah GP telemetry synced to database!"})

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)