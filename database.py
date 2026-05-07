import sqlite3

def get_connection():
    conn = sqlite3.connect("workout.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sesiones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            notas TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ejercicios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sesion_id INTEGER NOT NULL,
            nombre TEXT NOT NULL,
            series INTEGER NOT NULL,
            repeticiones INTEGER NOT NULL,
            peso REAL NOT NULL,
            FOREIGN KEY (sesion_id) REFERENCES sesiones(id)
        )
    """)

    conn.commit()
    conn.close()
