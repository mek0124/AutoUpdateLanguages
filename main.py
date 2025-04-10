from datetime import datetime, timedelta
from bs4 import BeautifulSoup

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


class AutoUpdateLanguages:
    def __init__(self):
        self.running = True
        self.current_month = 0

    async def start(self):
        print("Starting Language Update Loop... Please Wait...")

        while self.running: # keeps it running 24/7
            print("Loop Running")
            today = datetime.today()
            print(f"Today's Date: {today}")
            todays_month = today.month
            print(f"Today's Month #: {todays_month}")
            
            print("\nChecking if it's still the same month")
            if todays_month != self.current_month or self.current_month == 0:
                print("It is now a new month")
                print("Attempting to generate language list file")
                try:
                    print("Generating File... Please Wait...")
                    self.generate_file()
                    print("File Generated Successfully. Updating the stored current month variable for next check")
                    self.current_month = todays_month
                    print("Variable updated.")
                except Exception as e:
                    print("File Generation Failed. See Output\n")
                    print(e)
                    self.stop() # stop the program on error
            tomorrow = today + timedelta(days=1)
            print(f"\nStill the same month... Will Check Again on {tomorrow}...")
            # sleep for 1 day
            await asyncio.sleep(86400)

        
        # extra check to ensure the program exits given an error
        self.stop()

    def generate_file(self):
        curr_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(curr_dir, "languages.txt")

        current_unanitized_list = self.get_list_request()

        # if the file doesn't exist, create it for the first time
        if not os.path.exists(file_path):
            with open(file_path, 'w+') as file:
                for ul in current_unanitized_list:
                    for li in ul:
                        file.write(li.string)
        # overwrite the file each time after to avoid duplicates
        else:
            with open(file_path, 'w') as file:
                for ul in current_unanitized_list:
                    for li in ul:
                        file.write(li.string)

        print("finished updating lang file")

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

    def update_month(self):
        self.current_month += 1

        if self.current_month > 12:
            self.current_month = 0

        return self.current_month


if __name__ == '__main__':
    app = AutoUpdateLanguages()
    asyncio.run(app.start())
