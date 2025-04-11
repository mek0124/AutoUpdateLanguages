from datetime import datetime
from bs4 import BeautifulSoup
from functools import lru_cache

import requests
import asyncio
import json
import sys
import os


"""
For now, I am using https://programminglanguages.info/languages/
to pull the language list from. This URL can be replace, but the code
might have to be updated to match.
"""

# TODO
#! - cache fetched lang list
#? - Filter out dead, eso-langs, and unused

class AutoUpdateLanguages:
    def __init__(self):
        self.running = True
        self.current_month = 0
        self.cache_langs = [] # memory cache
        self.expire_days = 30

    async def start(self):
        print("Starting AutoUpdateLanguage Task...")

        today = datetime.today()
        todays_month = today.month
        month = todays_month
        day = today.day
        year = today.year

        next_month = datetime(year, month+1, day)

        print(f"Today: {today}")

        while self.running:
            if len(self.cache_langs) == 0:
                self.get_list_request()

            if todays_month != self.current_month:
                print("New Month. Re-Populating Language File...")
                self.get_list_request()
                self.generate_file()

                print(f"Updating stored month value to {todays_month}")
                self.current_month = todays_month
                print(f"Will update the file again on {next_month}")
                await asyncio.sleep(86400)
            else:
                print(f"Still the same month. Will check again on {next_month}")
                print("WARNING: If you are seeing this message, you should create a new issue on the repo's " \
                "issues page. This means that the loop is not tracking correctly -mek")
                self.stop()

        
        # extra check to ensure the program exits given an error
        self.stop()

    def generate_file(self):
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(curr_dir, "languages.txt")

        # if the file doesn't exist, create it for the first time
        if not os.path.exists(file_path):
            print("Creating language file for the first time... Please Wait...")
            with open(file_path, 'w+') as file:
                for ul in self.cache_langs:
                    for li in ul:
                        file.write(li.string)
            
            print("Language file created successfully")
        # overwrite the file each time after to avoid duplicates
        else:
            with open(file_path, 'w') as file:
                for ul in self.cache_langs:
                    for li in ul:
                        file.write(li.string)

    @lru_cache(maxsize=None)
    def get_list_request(self):
        url = "https://programminglanguages.info/languages/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find_all("ul", { "class": "column-list" })

    def match_lists(self, list_a: list, list_b: list):
        new_list = []

        for i in list_a:
            if list_a[i] not in list_b:
                new_list.append(list_a[i])

        for j in list_b:
            if list_b[j] not in list_a:
                new_list.append(list_b[j])

        return new_list

    def get_max_range(self, len_list_a: int, len_list_b: int) -> int:
        biggest = len_list_a

        if len_list_b > biggest:
            biggest = len_list_b

        return biggest

    def write_to_json(self, file_path: str, language_list: list):
        with open(file_path, 'w+', encoding="utf-8-sig") as f:
            json.dump(language_list, f, indent=2)

    def stop(self):
        self.running = False
        sys.exit(0)


if __name__ == '__main__':
    app = AutoUpdateLanguages()
    asyncio.run(app.start())
