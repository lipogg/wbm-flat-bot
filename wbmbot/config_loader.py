import yaml
import logging
from pathlib import Path

logger = logging.getLogger("app")

class ConfigLoader:
    def __init__(self, config_path="config.yaml"):
        self.config_path = Path(config_path)

    def load_user_data(self):
        # read in config file if exists
        if self.config_path.is_file():
            logger.info(f"Loading config from {self.config_path}...")
            with self.config_path.open("r") as f:
                try:
                    config = yaml.safe_load(f)
                except yaml.YAMLError as e:
                    print(f"[{date()}] YAML error: {e}")
                    raise
        else:
            logger.info(f"No config file found. Terminating...")
            raise FileNotFoundError(f"{self.config_path} does not exist.")

        return config