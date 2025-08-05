from wbmbot.utils import setup_loggers

setup_loggers()

import logging
logger = logging.getLogger("app")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from wbmbot import User, ConfigLoader, FlatScraper, ApplicationManager


def main():
    # Load or interactively collect user data/configuration
    user_input = ConfigLoader(config_var="USER_CONFIG")
    user_data = user_input.load_user_data()
    user = User(user_data)

    # Configure Chrome WebDriver options
    options = Options()
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--headless=new")
    options.add_argument('--log-level=3')

    with webdriver.Chrome(options=options) as driver:
        driver.implicitly_wait(5)
        start_url = "https://www.wbm.de/wohnungen-berlin/angebote/"

        # Initialize application handler
        app_manager = ApplicationManager(driver, user)

        # Initialize scraper and load starting page
        scraper = FlatScraper(driver, start_url)
        scraper.load_start_page()

        # Scrape flats from the website
        flats = scraper.get_flats()

        # Iterate over flats and apply if they match user criteria
        for flat in flats:
            if flat.matches_criteria(user):
                flat_details = scraper.get_details(flat)
                flat.update_details(flat_details)
                if flat.within_range(user):
                    logger.info(f"Flat {flat.title} matches criteria... applying...")
                    app_manager.apply(flat)
            else:
                logger.info(f"Flat '{flat.title}' does not meet search criteria... skipping...")


if __name__ == "__main__":
    main()