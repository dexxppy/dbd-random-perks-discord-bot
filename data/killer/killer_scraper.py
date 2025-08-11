import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from killer_page_links import links

load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

killers = ["All Killers"]
perks = []
addons = [[]]

general_perks_link = "https://deadbydaylight.fandom.com/wiki/Perks/General_Perks"

try:
    driver.get(general_perks_link)
    time.sleep(2)

    table = driver.find_elements(By.XPATH, '//table[contains(@class, "wikitable")]')[1]
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

    perks.append(vals)

except Exception as e:
    print(f"Error processing general perks link: {e}")

for link in links:
    try:
        driver.get(link[0])
        time.sleep(2)

        parent_div = driver.find_element(By.XPATH, '//div[contains(@class, "page-header__title")]')
        child_div = parent_div.find_element(By.XPATH, './/h1')

        killer_name = child_div.text.strip().split(' — ')
        if len(killer_name) > 1:
            killers.append(killer_name[1])
        else:
            killers.append(killer_name[0])

        table_divs = driver.find_elements(By.XPATH, '//table[contains(@class, "wikitable")]')
        table_divs = [table_divs[link[1]], table_divs[link[2]]] # only perks and addons tables

        for table in table_divs:
            time.sleep(1)
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

            if table == table_divs[0]:  # perks table
                perks.append(vals)
            elif table == table_divs[1]:  # addons table
                addons.append(vals)

    except Exception as e:
        print(f"Error processing link {link}: {e}")

driver.quit()

list = []

addons_dicts = []

for addon in addons:
    addon_list = []
    for addon_name in addon:
        addon_list.append({"addon_name": addon_name, "addon_rarity": "Common/Uncommon/Rare/Very Rare/Ultra Rare"})
    addons_dicts.append(addon_list)

for killer, perk_list, addon_list in zip(killers, perks, addons_dicts):
    list.append({
        "killer_name": killer,
        "killer_perks": perk_list,
        "killer_addons": addon_list
    })

with open('./data/killer/killers_list.json', 'w', encoding='utf-8') as f:
    json.dump(list, f, ensure_ascii=False, indent=4)

