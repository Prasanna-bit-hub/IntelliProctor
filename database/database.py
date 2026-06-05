import sqlite3

DATABASE_NAME = "database/intelliproctor.db"


def get_connection():

    conn = sqlite3.connect(
        DATABASE_NAME,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            timestamp TEXT,

            alert_type TEXT,

            severity TEXT,

            snapshot_path TEXT

        )

    """)

    conn.commit()

    conn.close()


def insert_alert(
    timestamp,
    alert_type,
    severity,
    snapshot_path
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO alerts (
            timestamp,
            alert_type,
            severity,
            snapshot_path
        )

        VALUES (?, ?, ?, ?)

    """, (
        timestamp,
        alert_type,
        severity,
        snapshot_path
    ))

    conn.commit()

    conn.close()


def fetch_alerts():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM alerts
        ORDER BY id DESC

    """)

    alerts = cursor.fetchall()

    conn.close()

    return [
        dict(alert)
        for alert in alerts
    ]