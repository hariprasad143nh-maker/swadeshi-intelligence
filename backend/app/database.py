import sqlite3
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "swadeshi.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hs_code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        sector TEXT NOT NULL,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS import_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        financial_year TEXT NOT NULL,
        country TEXT DEFAULT 'World',
        import_value_usd REAL NOT NULL,
        quantity REAL,
        unit TEXT NOT NULL,
        source TEXT DEFAULT 'Government Trade Analytics Portal',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(product_id, financial_year, country)
    );

    CREATE TABLE IF NOT EXISTS production_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL UNIQUE REFERENCES products(id) ON DELETE CASCADE,
        import_cost REAL NOT NULL,
        domestic_cost REAL NOT NULL,
        feasibility_score REAL NOT NULL,
        confidence TEXT DEFAULT 'medium',
        evidence TEXT,
        cost_basis TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS production_regions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
        state TEXT NOT NULL,
        district TEXT NOT NULL,
        suitability_score REAL NOT NULL,
        suitability_reason TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


# Ensure DB tables exist on import
init_db()
