import logging
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from .models import Flat

logger = logging.getLogger("app")

class FlatScraper:
    def __init__(self, driver, start_url):
        self.driver = driver
        self.start_url = start_url

    def load_start_page(self):
        logger.info(f"Connecting to {self.start_url}")
        self.driver.get(self.start_url)
        self._accept_cookies()
        self._scroll_to_footer()

    def _accept_cookies(self):
        if self.driver.find_elements(By.CLASS_NAME, 'cn-buttons'):
            logger.info("Accepting cookies...")
            self.driver.find_element(By.CLASS_NAME, 'cn-decline').click()

    def _scroll_to_footer(self):
        footer = self.driver.find_element(By.TAG_NAME, 'footer')
        ActionChains(self.driver).scroll_to_element(footer).perform()

    def get_flats(self):
        logger.info("Searching flats...")
        flat_elements = self.driver.find_elements(By.CSS_SELECTOR, ".row.openimmo-search-list-item")
        flats = []
        for elem in flat_elements:
            # Extract summary attributes
            summary_attrs = self._extract_summary_attributes(elem)
            flat = Flat(summary_attrs)
            flats.append(flat)

        return flats

    def get_details(self, detail_link):
        # Navigate to details page and extract details from detail page
        self.driver.get(detail_link)
        detail_attrs = self._extract_detail_attributes()
        return detail_attrs


    def _extract_summary_attributes(self, flat_elem):
        # Extract title, total rent, size, rooms, zip_code, property attributes summary from flat_elem, link to detail page
        title = self._find_element_safe(flat_elem, By.CLASS_NAME, 'imageTitle')
        total_rent = self._find_element_safe(flat_elem, By.CLASS_NAME, 'main-property-rent')
        size = self._find_element_safe(flat_elem, By.CLASS_NAME, 'main-property-size')
        rooms = self._find_element_safe(flat_elem, By.CLASS_NAME, 'main-property-rooms')
        zip_code = self._find_element_safe(flat_elem, By.CLASS_NAME, 'address')
        property_attrs_elems = flat_elem.find_elements(By.XPATH, './/ul[@class="check-property-list"]/li')
        property_attrs = [elem.text for elem in property_attrs_elems]
        detail_link = flat_elem.find_element(By.XPATH, '//*[@title="Details"]').get_attribute('href') # always exists, no safeguard here

        return {
            "title": title,
            "total_rent": total_rent,
            "size": size,
            "rooms": rooms,
            "zip_code": zip_code,
            "property_attrs": property_attrs,
            "detail_url": detail_link,
        }

    def _extract_detail_attributes(self):
        # Extract the detail page specific fields like base_rent and others
        base_rent = self._find_element_safe(self.driver, By.CLASS_NAME, 'openimmo-detail__rental-costs-list-item-value')
        return {
            "base_rent": base_rent,
            # maybe add floor here
        }

    @staticmethod
    def _find_element_safe(elem, by, value, fallback=""):
        try:
            return elem.find_element(by, value).text
        except NoSuchElementException:
            return fallback
