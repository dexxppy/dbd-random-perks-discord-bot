import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv
from survivor_page_links import links

load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

survs = ["All Survivors"]
perks = []

general_perks_link = "https://deadbydaylight.fandom.com/wiki/Perks/General_Perks"

try:
    driver.get(general_perks_link)
    time.sleep(2)

    table = driver.find_elements(By.XPATH, '//table[contains(@class, "wikitable")]')[0]
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
        surv_name = ""
        try:
            child_div = parent_div.find_element(By.XPATH, './/h1//span')
            surv_name = child_div.text.strip()

        except:
            try: 
                child_div = parent_div.find_element(By.XPATH, './/h1')
                surv_name = child_div.text.strip()
            except: 
                print(f"Error finding child div for link {link[0]}")

        surv_name = child_div.text.strip().split(' — ')[0]
        survs.append(surv_name)

        table_divs = driver.find_elements(By.XPATH, '//table[contains(@class, "wikitable")]')
        table_divs = [table_divs[link[1]]] # only perks table

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
            
            perks.append(vals)

    except Exception as e:
        print(f"Error processing link {link[0]}: {e}")

driver.quit()

list = []

for surv, perk_list in zip(survs, perks):
    list.append({
        "survivor_name": surv,
        "survivor_perks": perk_list,
    })


with open('./data/survivor/survivors_list.json', 'w', encoding='utf-8') as f:
    json.dump(list, f, ensure_ascii=False, indent=4)

