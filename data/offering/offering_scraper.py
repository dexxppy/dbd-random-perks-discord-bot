import time
import os
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from dotenv import load_dotenv

load_dotenv()
CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)

link = "https://www.unwrittenrulebook.com/offeringlist.html"

survivor_offerings = []
killer_offerings = []
all_offerings = []

try:
    driver.get(link)
    time.sleep(2)

    offerings_container = driver.find_element(By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "offering-container")]')
    offerings_divs = offerings_container.find_elements(By.XPATH, './/div[contains(@class, "item-type-section")]')

    for div in offerings_divs:
        list_div = div.find_element(By.XPATH, './/div[contains(@class, "survivor-list")]')
        list_subdivs = list_div.find_elements(By.CSS_SELECTOR, "div[class^='survivor-card']")

        for subdiv in list_subdivs:
            info_div = subdiv.find_element(By.XPATH, './/div[contains(@class, "survivor-info")]')
            offering_name = info_div.find_element(By.XPATH, './/h2[contains(@class, "survivor-name")]').text
            print(offering_name)
            badges = info_div.find_element(By.XPATH, './/div[contains(@class, "survivor-badges")]')
            offering_rarity = badges.find_element(By.CSS_SELECTOR, "span[class^='survivor-badge rarity-badge']").text
            offering_character_type = badges.find_element(By.CSS_SELECTOR, "span[class='survivor-badge']").text

            offering_data = {"offering_name": offering_name, "offering_rarity": offering_rarity}

            if offering_character_type == "Killer":
                killer_offerings.append(offering_data)
            elif offering_character_type == "Survivor":
                survivor_offerings.append(offering_data)
            elif offering_character_type == "All":
                all_offerings.append(offering_data)

except Exception as e:
    print(e)

driver.quit()

json_data = [
    {
        "character_type": "All",
        "offerings": all_offerings,
    },
    {
        "character_type": "Killer",
        "offerings": killer_offerings,
    },
    {
        "character_type": "Survivor",
        "offerings": survivor_offerings,
    }
]

with open('./data/offering/offerings_list.json', 'w', encoding='utf-8') as f:
    json.dump(json_data, f, ensure_ascii=False, indent=4)


