from pathlib import Path
import sqlite3


DB_PATH = Path("sensor_data.db")


def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def init_database():
    connection = get_db_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS nbiot_packets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            payload TEXT NOT NULL,
            ip TEXT,
            port INTEGER,
            received_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def row_to_dict(row):
    if row is None:
        return None

    return {
        "id": row["id"],
        "payload": row["payload"],
        "ip": row["ip"],
        "port": row["port"],
        "received_at": row["received_at"]
    }