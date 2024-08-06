import json
import os
from datetime import datetime

class Counter:
    def __init__(self, file, max_calls_per_day):
        self.COUNTER_FILE = os.path.join("counter_files", file)
        self.MAX_CALLS_PER_DAY = max_calls_per_day
        self.__ensure_directory_exists()
        pass

    def __ensure_directory_exists(self):
        directory = os.path.dirname(self.COUNTER_FILE)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def __read_counter(self):
        if os.path.exists(self.COUNTER_FILE):
            with open(self.COUNTER_FILE, "r") as file:
                return json.load(file)
        return {"date": str(datetime.now().date()), "count": 0}
    
    def __write_counter(self,counter):
        with open(self.COUNTER_FILE, "w") as file:
            json.dump(counter, file)

    def update_counter(self):
        counter = self.__read_counter()
        current_date = str(datetime.now().date())

        if counter["date"] != current_date:
            counter = {"date": current_date, "count": 0}

        if counter["count"] >= self.MAX_CALLS_PER_DAY:
            raise Exception("Daily limit reached")

        counter["count"] += 1
        self.__write_counter(counter)