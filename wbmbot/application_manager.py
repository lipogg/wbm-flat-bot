import os
import logging
from pathlib import Path
from selenium.webdriver.common.by import By

logger_app = logging.getLogger("app")
logger_flats = logging.getLogger("flats")

class ApplicationManager:
    def __init__(self, driver, user, log_path="logs/flats.log"):
        self.driver = driver
        self.user = user
        self.log_path = Path(log_path)

    def has_applied(self, flat_hash):
        with self.log_path.open("r", encoding="utf-8") as logfile:
            return flat_hash in logfile.read()

    def apply(self, flat):
        if self.has_applied(flat.hash):
            logger_app.info(f"Already applied for flat: {flat.title}")
            return False

        self._fill_form_and_submit(flat)
        self._log_application(flat)
        logger_app.info(f"Application submitted for: {flat.title}")
        return True

    def _fill_form_and_submit(self, flat):
        # works only if form is opened on flat's detail page already loaded in driver
        self.driver.find_element(By.XPATH, '//a[@class="openimmo-detail__contact-box-button btn scrollLink"]').click()
        self.driver.find_element(By.XPATH, '//*[@id="powermail_field_name"]').send_keys(self.user.last_name)
        self.driver.find_element(By.XPATH, '//*[@id="powermail_field_vorname"]').send_keys(self.user.first_name)
        self.driver.find_element(By.XPATH, '//*[@id="powermail_field_e_mail"]').send_keys(self.user.email)
        self.driver.find_element(By.XPATH, '//label[@for="powermail_field_datenschutzhinweis_1"]').click() # (By.XPATH, '//input[@id="powermail_field_datenschutzhinweis_1"]').click()
        self.driver.find_element(By.XPATH, '//button[@class="btn btn-primary" and @type="submit"]').click()

    def _log_application(self, flat):
        logger_flats.info(
            f"Application sent:\n"
            f"{flat.title}\n"
            f"zip code: {flat.zip_code}\n"
            f"total rent: {flat.total_rent}\n"
            f"flat size: {flat.size}\n"
            f"rooms: {flat.rooms}\n"
            f"wbs: {flat.wbs}\n"
            f"property attributes: {', '.join(flat.property_attrs)}\n"
            f"hash: {flat.hash}\n"
            f"user email: {self.user.email.strip()}\n\n"
        )