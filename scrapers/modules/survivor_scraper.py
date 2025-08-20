from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class SurvivorScraper(BaseScraper):
    def __init__(self, driver=None, link=None, output_file=None, wait_time=10):
        link = link or "https://www.unwrittenrulebook.com/survivorlist.html"
        output_file = output_file or "survivors.json"
        super().__init__(link=link, output_file=output_file, wait_time=wait_time, driver=driver)

    def scrape(self):
        survivors = []

        survivors_container = self.wait_for_element_presence(
            By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "survivor-container")]'
        )

        survivor_divs = self.wait_for_all_elements_presence(
            By.XPATH, './/div[contains(@class, "survivor-list")]//div[contains(@class, "survivor-card")]', survivors_container
        )

        for div in survivor_divs:
            info_div = div.find_element(By.XPATH, ".//div[contains(@class, 'survivor-info')]")
            survivor_name = self.get_elements_text(By.XPATH, ".//h2[contains(@class, 'survivor-name')]", info_div)
            survivors.append({"survivor_name": survivor_name})

        return survivors