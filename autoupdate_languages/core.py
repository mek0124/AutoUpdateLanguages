from datetime import datetime
from bs4 import BeautifulSoup

import requests
import asyncio
import os


class AutoUpdateLanguages:
    def __init__(self):
        self.day_count = 1
        self.exp_days = 30
        self.delay = 86400 # 1 day in seconds
        self.url = "https://programminglanguages.info/languages/"

    async def start(self):
        output_dir = await self.check_for_output_dir()
        await self.generate_file(output_dir)
        await self.start_sequence(output_dir)

    async def check_for_output_dir(self):
        proj_root_dir = os.path.abspath(os.path.dirname(__file__))
        output_dir = os.path.join(proj_root_dir, "project_output")

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)

        return output_dir

    async def generate_file(self, output_dir):
        output_file = os.path.join(output_dir, "lang_list.txt")

        lang_list = await self.get_lang_list()

        with open(output_file, 'w') as lang_file:
            for ul in lang_list:
                for li in ul:
                    if li:
                        lang_file.write(li.string)

    async def start_sequence(self, output_dir):
        today, next_month = await self.get_dates()

        print(f"Today: {today}")

        while self.day_count < self.exp_days:
            remaining_days = self.exp_days - self.day_count
            print(f"Day #{self.day_count}) File Update In {remaining_days} days on {next_month}")
            
            await asyncio.sleep(self.delay)
            self.day_count += 1
        else:
            await self.generate_file(output_dir)

    async def get_dates(self) -> tuple:
        today = datetime.now()
        next_month = datetime(
            today.year,
            today.month + 1,
            today.day
        )

        return (today, next_month)
    
    async def get_lang_list(self):
        url = "https://programminglanguages.info/languages/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html5lib')
        return soup.find_all("ul", { "class": "column-list" })
    

if __name__ == '__main__':
    app = AutoUpdateLanguages()
    asyncio.run(app.start())
