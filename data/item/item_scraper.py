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

link = "https://www.unwrittenrulebook.com/itemlist.html"

all_items = []

try:
    driver.get(link)
    time.sleep(2)

    items_container = driver.find_element(By.XPATH,
                                              './/section[contains(@class, "container")]//div[contains(@id, "item-container")]')
    items_divs = items_container.find_elements(By.XPATH, './/div[contains(@class, "item-type-section")]')

    for div in items_divs:
        item_family = div.find_element(By.XPATH, './/h2[contains(@class, "item-type-header")]').text

        list_div = div.find_element(By.XPATH, './/div[contains(@class, "survivor-list")]')
        list_subdivs = list_div.find_elements(By.CSS_SELECTOR, "div[class^='survivor-card']")

        addons = []
        items = []

        first = True

        for subdiv in list_subdivs:
            info_div = subdiv.find_element(By.XPATH, ".//div[contains(@class, 'survivor-info')]")

            if first:
                addons_btn = info_div.find_elements(By.XPATH, ".//div[contains(@class, 'popup-buttons')]//button")[1]
                addons_btn.click()
                time.sleep(1)

                popup_div = driver.find_element(By.XPATH,
                                                ".//div[contains(@id, 'addonsPopup')]"
                                                "//div[contains(@class, 'popup-content')]")
                addons_div = popup_div.find_element(By.XPATH, "//div[contains(@id, 'addonsPopupContent')]"
                                                "//div[contains(@class, 'perk-list')]")
                addon_divs = addons_div.find_elements(By.CSS_SELECTOR, "div[class^='perk-item']")

                for addon_div in addon_divs:
                    details_div = addon_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-details')]//div[contains(@class, 'perk-name')]")

                    addon_name = driver.execute_script("""
                        let element = arguments[0];
                        let childSpans = element.querySelectorAll('span');
                        let text = element.childNodes[0].nodeValue.trim();
                        return text;
                    """, details_div)

                    addon_rarity = div.find_element(By.TAG_NAME, "span").text

                    addons.append({"survivor_addon_name": addon_name, "survivor_addon_rarity": addon_rarity})

                first = False
                popup_div.find_element(By.XPATH, ".//button[contains(@class, 'popup-close')]").click()
                time.sleep(1)

            item_name = info_div.find_element(By.XPATH, ".//h2").text
            item_rarity = info_div.find_element(By.XPATH, ".//div[contains(@class, 'survivor-badges')]//span").text

            items.append({"survivor_item_name": item_name, "survivor_item_rarity": item_rarity})

        list = {
            "survivor_item_family": item_family,
            "survivor_items": items,
            "survivor_addons": addons
        }

        all_items.append(list)

    driver.quit()

except Exception as e:
    print(e)

with open('./data/item/items_list.json', 'w', encoding='utf-8') as f:
    json.dump(all_items, f, ensure_ascii=False, indent=4)




