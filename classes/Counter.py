import sqlite3
import os
from datetime import datetime

class Counter:
    def __init__(self, db_file, max_calls_per_day):
        self.DB_FILE = os.path.join("counter_files", db_file)
        self.MAX_CALLS_PER_DAY = max_calls_per_day
        self.__ensure_directory_exists()
        self.__initialize_db()

    def __initialize_db(self):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS counter (
                    date TEXT PRIMARY KEY,
                    count INTEGER
                )
            ''')
            conn.commit()

    def __ensure_directory_exists(self):
        directory = os.path.dirname(self.DB_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    def __read_counter(self):
        current_date = str(datetime.now().date())
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT count FROM counter WHERE date = ?', (current_date,))
            row = cursor.fetchone()
            if row:
                return {"date": current_date, "count": row[0]}
            return {"date": current_date, "count": 0}

    def __write_counter(self, counter):
        with sqlite3.connect(self.DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO counter (date, count) VALUES (?, ?)
                ON CONFLICT(date) DO UPDATE SET count = excluded.count
            ''', (counter["date"], counter["count"]))
            conn.commit()

    def __testing_counter(self):
        db_file = self.DB_FILE
        new_value = 81
        current_date = str(datetime.now().date())
        with sqlite3.connect(db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO counter (date, count) VALUES (?, ?)
                ON CONFLICT(date) DO UPDATE SET count = excluded.count
            ''', (current_date, new_value))
            conn.commit()

    def update_counter(self):
        self.__testing_counter()
        counter = self.__read_counter()
        current_date = str(datetime.now().date())

        if counter["date"] != current_date:
            counter = {"date": current_date, "count": 0}

        if counter["count"] >= self.MAX_CALLS_PER_DAY:
            raise Exception("Daily limit reached")

        counter["count"] += 1
        self.__write_counter(counter)