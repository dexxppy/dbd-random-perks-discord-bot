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

link = "https://www.unwrittenrulebook.com/survivorlist.html"

survivors = []

try:
    driver.get(link)
    time.sleep(2)

    survivors_container = driver.find_element(By.XPATH,
                                              './/section[contains(@class, "container")]//div[contains(@id, "survivor-container")]')
    survivor_divs = survivors_container.find_elements(By.XPATH, '//div[contains(@class, "survivor-list")]'
                                                             '//div[contains(@class, "survivor-card")]')
    for div in survivor_divs:
        perks = []

        info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'survivor-info')]")
        survivor_name = info_div.find_element(By.TAG_NAME, "h2").text

        popup_button = info_div.find_elements(By.XPATH, './/div[contains(@class, "popup-buttons")]//button')[1]

        # get perks
        popup_button.click()
        time.sleep(1)
        popup_container = driver.find_element(By.XPATH, './/div[contains(@id, "perksPopup")]//div[contains(@class, "popup-content")]')

        perks_container = popup_container.find_element(By.XPATH, './/div[contains(@id, "perksContent")]//div[contains(@class, "perk-list")]')
        perks_divs = perks_container.find_elements(By.XPATH, './/div[contains(@class, "perk-item")]')

        for perk_div in perks_divs:
            perk_name = perk_div.find_element(By.XPATH, './/div[contains(@class, "perk-details")]//div[contains(@class, "perk-name")]').text
            perks.append(perk_name)

        popup_container.find_element(By.XPATH, './/button[contains(@class, "popup-close")]').click()
        time.sleep(1)

        survivors.append({"survivor_name": survivor_name, "survivor_perks": perks})

    driver.quit()

except Exception as e:
    print(e)

with open('./data/survivor/survivors_list.json', 'w', encoding='utf-8') as f:
    json.dump(survivors, f, ensure_ascii=False, indent=4)

