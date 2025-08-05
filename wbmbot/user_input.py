import os
import yaml
import logging

logger = logging.getLogger("app")

# user prompts adapted from https://github.com/fischer-hub/wbmbot
class UserInput:
    def __init__(self, config_path="config.yaml"):
        self.config_path = config_path

    def load_user_data(self):
        # read in config file if exists
        if os.path.isfile(self.config_path):
            logger.info(f"Loading config from {self.config_path}...")
            with open(self.config_path, "r") as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"[{date()}] YAML error: {e}")
                    raise
        # if not: make config file from user input
        else:
            logger.info(f"No config file found. Starting interactive setup...")
            config = self._collect_user_input()
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            logger.info(f"Config written to {self.config_path}.")

        return config

    @staticmethod
    def _collect_user_input():
        data = {
            "first_name": input("Please input your first name and confirm with enter: "),
            "last_name": input("Please input your last name and confirm with enter: "),
            "email": input("Please input your email address and confirm with enter: "),
            "wbs": input("Do you have a WBS (Wohnberechtigungsschein)?\nPlease type yes / no: "),
            "net_income": input("Please input your net household income (rounded down to the nearest full number) and confirm with enter: "),
            "min_rooms": input("Please input the minimum number of rooms and confirm with enter: "),
            "min_sqm": input("Please input the minimum size in square metres and confirm with enter: "),
            "max_rent": input("Please input the maximum rent and confirm with enter: "),
        }

        if 'yes' in input("Do you want to enter keywords to filter for specific flats?\nPlease type yes / no: "):
            kw_filter = []
            while True:
                keyword = input("Enter keyword (e.g. 'balcony'), or 'exit': ")
                if keyword.strip().lower() == 'exit':
                    break
                kw_filter.append(keyword.strip().lower())
            data['kw_filter'] = kw_filter
        else:
            data['kw_filter'] = []

        if 'yes' in input("Do you want to restrict search to certain zip codes?\nPlease type yes / no: "):
            loc_filter = []
            while True:
                code = input("Enter ZIP code or prefix, or 'exit': ")
                if code.strip().lower() == 'exit':
                    break
                loc_filter.append(code.strip().lower())
            data['loc_filter'] = loc_filter
        else:
            data['loc_filter'] = []

        return data