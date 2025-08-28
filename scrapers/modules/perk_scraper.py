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
                perk_icon = (div.find_element(By.XPATH, ".//div[contains(@class, 'perk-image-container')]//img")
                             .get_attribute("src"))
                info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'perk-info')]")
                perk_name = info_div.find_element(By.XPATH, ".//h3[contains(@class, 'perk-name')]").text
                owner = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-owner')]").text.split(": ")[1]
                character_type = info_div.find_element(By.XPATH, ".//div[contains(@class, 'perk-badges')]//span").text

                if "Common" in owner:
                    owner = f"All {character_type}s"

                if character_type == "Killer":
                    killer_perks.append({"killer_perk_name": perk_name,
                                         "killer_owner_name": owner,
                                         "killer_perk_icon": perk_icon})
                elif character_type == "Survivor":
                    survivor_perks.append({"survivor_perk_name": perk_name,
                                           "survivor_owner_name": owner,
                                           "survivor_perk_icon": perk_icon})

            next_button = self.driver.find_element(By.XPATH,
                                                    './/div[contains(@id,"pagination")]//button[contains(text(),"»")]')
            if next_button.get_attribute("disabled") is not None:
                last_page = True

        return {"survivor_perks": survivor_perks, "killer_perks": killer_perks}
