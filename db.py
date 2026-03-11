import sqlite3

DB_NAME = "activity_log.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def setup_db():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            frequency TEXT NOT NULL,
            schedule TEXT,
            reminder_time TEXT,
            track_duration INTEGER DEFAULT 0,
            track_quantity INTEGER DEFAULT 0,
            track_satisfaction INTEGER DEFAULT 0,
            timestamp TEXT NOT NULL,
        )
    ''')
    
    cur.execute('''
    CREATE TABLE IF NOT EXISTS daily_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        activity_id INTEGER NOT NULL,
        completed INTEGER DEFAULT 0,
        time TEXT,
        duration TEXT,
        quantity TEXT,
        satisfaction INTEGER,
        notes TEXT,
        FOREIGN KEY (activity_id) REFERENCES activities(id
    )           
    ''')
    conn.commit()
    conn.close()