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

link = "https://www.unwrittenrulebook.com/killerlist.html"

killers = []

try:
    driver.get(link)
    time.sleep(2)

    killers_container = driver.find_element(By.XPATH,
                                              './/section[contains(@class, "container")]//div[contains(@id, "killer-container")]')
    killers_divs = killers_container.find_elements(By.XPATH, '//div[contains(@class, "survivor-list")]'
                                                             '//div[contains(@class, "survivor-card")]')
    for div in killers_divs:
        perks = []
        addons = []

        info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'survivor-info')]")
        killer_name = driver.execute_script("""
                        let element = arguments[0];
                        let childSpans = element.querySelectorAll('span');
                        let text = element.childNodes[0].nodeValue.trim();
                        return text;
                    """, info_div.find_element(By.TAG_NAME, 'h2'))

        popup_buttons = info_div.find_elements(By.XPATH, './/div[contains(@class, "popup-buttons")]//button')

        # get perks
        popup_buttons[2].click()
        time.sleep(1)
        popup_container = driver.find_element(By.XPATH, './/div[contains(@id, "perksPopup")]//div[contains(@class, "popup-content")]')

        perks_container = popup_container.find_element(By.XPATH, './/div[contains(@id, "perksContent")]//div[contains(@class, "perk-list")]')
        perks_divs = perks_container.find_elements(By.XPATH, './/div[contains(@class, "perk-item")]')

        for perk_div in perks_divs:
            perk_name = perk_div.find_element(By.XPATH, './/div[contains(@class, "perk-details")]//div[contains(@class, "perk-name")]').text
            perks.append(perk_name)

        popup_container.find_element(By.XPATH, './/button[contains(@class, "popup-close")]').click()
        time.sleep(1)

        # get addons
        popup_buttons[3].click()
        time.sleep(1)
        popup_container = driver.find_element(By.XPATH, './/div[contains(@id, "addonsPopup")]//div[contains(@class, "popup-content")]')

        addons_container = popup_container.find_element(By.XPATH, './/div[contains(@id, "addonsContent")]//div[contains(@class, "perk-list")]')
        addons_divs = addons_container.find_elements(By.CSS_SELECTOR, 'div[class^="perk-item"]')

        for addon_div in addons_divs:
            details_div = addon_div.find_element(By.XPATH, './/div[contains(@class, "perk-details")]//div[contains(@class, "perk-name")]')
            addon_name = driver.execute_script("""
                let element = arguments[0];
                let childSpans = element.querySelectorAll('span');
                let text = element.childNodes[0].nodeValue.trim();
                return text;
            """, details_div)

            addon_rarity = details_div.find_element(By.TAG_NAME, "span").text
            addons.append({"addon_name": addon_name, "addon_rarity": addon_rarity})

        popup_container.find_element(By.XPATH, './/button[contains(@class, "popup-close")]').click()
        time.sleep(1)

        killers.append({"killer_name": killer_name, "killer_perks": perks, "killer_addons": addons})

    driver.quit()

except Exception as e:
    print(e)

with open('./data/killer/killers_list.json', 'w', encoding='utf-8') as f:
    json.dump(killers, f, ensure_ascii=False, indent=4)



