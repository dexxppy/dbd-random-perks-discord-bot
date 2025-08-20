from scrapers.base_scraper import BaseScraper
from selenium.webdriver.common.by import By

class KillerScraper(BaseScraper):
    def __init__(self, link=None, output_file=None, wait_time=10, driver=None):
        link = link or "https://www.unwrittenrulebook.com/killerlist.html"
        output_file = output_file or "killers.json"
        super().__init__(link=link, output_file=output_file, wait_time=wait_time, driver=driver)

    def scrape(self):
        killers = []

        killers_container = self.wait_for_element_presence(
            By.XPATH, './/section[contains(@class, "container")]//div[contains(@id, "killer-container")]'
        )

        killers_divs = self.wait_for_all_elements_presence(By.XPATH,
                                                            '//div[contains(@class, "survivor-list")]'
                                                                   '//div[contains(@class, "survivor-card")]',
                                                           killers_container
        )

        for div in killers_divs:
            addons = []

            info_div = self.wait_for_element_presence(By.XPATH, ".//div[contains(@class, 'survivor-info')]", div)

            killer_name = self.driver.execute_script("""
                                     let element = arguments[0];
                                     let childSpans = element.querySelectorAll('span');
                                     let text = element.childNodes[0].nodeValue.trim();
                                     return text;
                                 """, info_div.find_element(By.TAG_NAME, 'h2'))

            addons_btn = self.wait_for_element_to_be_clickable(By.XPATH,
                                                           ".//div[contains(@class, 'popup-buttons')]"
                                                                  "//button[contains(text(),'View Addons')]",
                                                                  info_div)

            addons_btn.click()
            popup_div = self.wait_for_element_presence(By.XPATH,
                                                './/div[contains(@id, "addonsPopup")]'
                                                       '//div[contains(@class, "popup-content")]')

            addons_container = popup_div.find_element(By.XPATH, './/div[contains(@id, "addonsContent")]'
                                                                '//div[contains(@class, "perk-list")]')
            addons_divs = addons_container.find_elements(By.CSS_SELECTOR, 'div[class^="perk-item"]')

            for addon_div in addons_divs:
                details_div = addon_div.find_element(By.XPATH, './/div[contains(@class, "perk-details")]//div[contains(@class, "perk-name")]')
                addon_name = self.driver.execute_script("""
                    let element = arguments[0];
                    let childSpans = element.querySelectorAll('span');
                    let text = element.childNodes[0].nodeValue.trim();
                    return text;
                """, details_div)

                addon_rarity = details_div.find_element(By.TAG_NAME, "span").text
                addons.append({"killer_addon_name": addon_name, "killer_addon_rarity": addon_rarity})

            popup_div.find_element(By.XPATH, './/button[contains(@class, "popup-close")]').click()
            killers.append({"killer_name": killer_name, "killer_addons": addons})

        return killers
