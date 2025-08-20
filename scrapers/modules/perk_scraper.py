from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class PerkScraper(BaseScraper):
    def __init__(self, link=None, output_file=None, wait_time=10, driver=None):
        link = link or "https://www.unwrittenrulebook.com/perklist.html"
        output_file = output_file or "perks.json"
        super().__init__(link=link, output_file=output_file, wait_time=wait_time, driver=driver)

    def scrape(self):
        last_page = False
        survivor_perks, killer_perks = [], []

        while not last_page:
            next_button = self.wait_for_element_to_be_clickable(By.XPATH, './/div[contains(@id,"pagination")]//button[contains(text(),"»")]')
            next_button.click()

            perks_container = self.wait_for_element_presence(
                By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "perk-container")]'
            )

            perks_divs = perks_container.find_elements(
                By.XPATH, './/div[contains(@class, "perk-list")]//div[contains(@class, "perk-card")]'
            )

            for div in perks_divs:
                info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'perk-info')]")
                perk_name = info_div.find_element(By.XPATH, ".//h3[contains(@class, 'perk-name')]").text
                owner = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-owner')]").text.split(": ")[1]
                character_type = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-badges')]//span").text

                if owner == "Common Perk":
                    owner = f"All {character_type}s"

                if character_type == "Killer":
                    killer_perks.append({"killer_perk_name": perk_name, "killer_owner_name": owner})
                elif character_type == "Survivor":
                    survivor_perks.append({"survivor_perk_name": perk_name, "survivor_owner_name": owner})

            next_button = self.driver.find_element(By.XPATH,
                                                    './/div[contains(@id,"pagination")]//button[contains(text(),"»")]')
            if next_button.get_attribute("disabled") is not None:
                last_page = True

        return {"survivor_perks": survivor_perks, "killer_perks": killer_perks}

# import os
# import json
#
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from dotenv import load_dotenv
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
# load_dotenv()
# CHROMEDRIVER_PATH = os.getenv('CHROMEDRIVER_PATH')
#
# service = Service(CHROMEDRIVER_PATH)
# driver = webdriver.Chrome(service=service)
#
# link = "https://www.unwrittenrulebook.com/perklist.html"
#
# survivor_perks = []
# killer_perks = []
#
# try:
#     driver.get(link)
#
#     last_page = False
#
#     while not last_page:
#         next_page_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, './/div[contains(@id,"pagination")]//button[contains(text(),"»")]'))
#         )
#         next_page_button.click()
#
#         perks_container = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located(
#                 (By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "perk-container")]'))
#         )
#         perks_divs = perks_container.find_elements(By.XPATH,
#                                                    './/div[contains(@class, "perk-list")]//div[contains(@class, "perk-card")]')
#         for div in perks_divs:
#             info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'perk-info')]")
#             perk_name = info_div.find_element(By.XPATH, ".//h3[contains(@class, 'perk-name')]").text
#             owner = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-owner')]").text.split(": ")[1]
#             character_type = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-badges')]//span").text
#
#             if owner == "Common Perk":
#                 owner = f'All {character_type}s'
#
#             if character_type == "Killer":
#                 killer_perks.append({"killer_perk_name": perk_name, "killer_owner_name": owner})
#             elif character_type == "Survivor":
#                 survivor_perks.append({"survivor_perk_name": perk_name, "survivor_owner_name": owner})
#
#         next_page_button = driver.find_element(By.XPATH,
#                                                './/div[contains(@id,"pagination")]//button[contains(text(),"»")]')
#         if next_page_button.get_attribute("disabled") is not None:
#             last_page = True
#
#     driver.quit()
#
#     perks = {
#         "survivor_perks": survivor_perks,
#         "killer_perks": killer_perks,
#     }
#
#     BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#     DATA_DIR = os.path.join(BASE_DIR, "data")
#
#     os.makedirs(DATA_DIR, exist_ok=True)
#
#     file_path = os.path.join(DATA_DIR, "perks.json")
#
#     with open(file_path, 'w', encoding='utf-8') as f:
#         json.dump(perks, f, ensure_ascii=False, indent=4)
#
# except Exception as e:
#     print(e)
#
#
