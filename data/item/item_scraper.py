import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from addon_page_links import links

load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

addons = []

try:
    for link in links:
        driver.get(link)
        time.sleep(2)

        table_container = driver.find_elements(By.XPATH, '//div[contains(@class, "tabber wds-tabber")]')[1]
        table = table_container.find_element(By.XPATH, './/div[contains(@class, "wds-tab__content wds-is-current")]').find_element(By.XPATH, './/table[contains(@class, "wikitable")]')

        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        vals = []

        for row in rows:
            ths = row.find_elements(By.TAG_NAME, 'th')
            try:
                for th in ths:
                    a = th.find_element(By.TAG_NAME, 'a')
                    name = a.text.strip()

                    if name != '':
                        vals.append(name)

            except Exception as e:
                continue
                
        addons.append(vals)

except Exception as e:
    print(f"Error ocurred with addons: {e}")

items = []
item_tables_indexes = [2, 3, 4, 5, 6]

driver.get("https://deadbydaylight.fandom.com/wiki/Items")
time.sleep(2)

try:
    table_divs = driver.find_elements(By.XPATH, '//table[contains(@class, "wikitable")]')
    table_divs = [table_divs[index] for index in item_tables_indexes] # only items tables

    for table in table_divs:
        time.sleep(2)
        tbody = table.find_element(By.TAG_NAME, 'tbody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')
        vals = []

        for row in rows:
            ths = row.find_elements(By.TAG_NAME, 'th')
            try:
                for th in ths:
                    a = th.find_element(By.TAG_NAME, 'a')
                    name = a.text.strip()

                    if name != '':
                        vals.append(name)

            except Exception as e:
                continue
            
        items.append(vals)

except Exception as e:
    print(f"Error ocurred with items: {e}")

driver.quit()

addons_dict_list = []

for addon_row in addons:
    mapped_row = []

    for addon in addon_row:
        mapped_row.append({
            "addon_name": addon,
            "addon_rarity": "",
        })

    addons_dict_list.append(mapped_row)

list = []

for item_row, addons_dicts in zip(items, addons_dict_list):
    for item in item_row:
        list.append({
            "item_name": item,
            "item_rarity": "",
            "item_addons_set": addons_dicts
        })
        

with open('items_list.json', 'w', encoding='utf-8') as f:
    json.dump(list, f, ensure_ascii=False, indent=4)

