from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TextNotEmpty:
    """Custom Expected Condition: wait until element has non-empty .text"""
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        element = driver.find_element(*self.locator)
        if element.text.strip() != "":
            return element
        return False


def wait_for_non_empty_text(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(TextNotEmpty(locator))
