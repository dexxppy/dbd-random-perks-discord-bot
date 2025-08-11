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

item_families = ["Flashlights", "Keys", "Maps", "Med-kits", "Toolboxes"]

addons = []

try:
    family_index = 0

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

        addons.append({"item_family": item_families[family_index], "addons": vals})
        family_index += 1

except Exception as e:
    print(f"Error ocurred with addons: {e}")

items = []
item_tables_indexes = [2, 3, 4, 5, 6]

driver.get("https://deadbydaylight.fandom.com/wiki/Items")
time.sleep(2)

try:
    family_index = 0
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

        items.append({"item_family": item_families[family_index], "items": vals})
        family_index += 1

except Exception as e:
    print(f"Error ocurred with items: {e}")

driver.quit()

families_dict_list = []

for addons_data_row, item_data_row in zip(addons, items):
    addons_values = addons_data_row["addons"]
    items_values = item_data_row["items"]
    mapped_row_addons = []
    mapped_row_items = []


    for addon in addons_values:
        mapped_row_addons.append({
            "addon_name": addon,
            "addon_rarity": "Common/Uncommon/Rare/Very Rare/Ultra Rare",
        })

    for item in items_values:
        mapped_row_items.append({
            "item_name": item,
            "item_rarity": "Common/Uncommon/Rare/Very Rare/Ultra Rare",
        })

    families_dict_list.append({"item_family": addons_data_row["item_family"],
                             "items": mapped_row_items,
                             "addons": mapped_row_addons
                             })
        

with open('./data/item/items_list.json', 'w', encoding='utf-8') as f:
    json.dump(families_dict_list, f, ensure_ascii=False, indent=4)

