import logging
from pathlib import Path

def setup_loggers():
    Path("logs").mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # File handler for app.log
    app_handler = logging.FileHandler("logs/app.log", encoding="utf-8")
    app_handler.setFormatter(formatter)

    # File handler for flats.log
    flats_handler = logging.FileHandler("logs/flats.log", encoding="utf-8")
    flats_handler.setFormatter(formatter)

    # Set up the 'app' logger
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.INFO)
    app_logger.addHandler(app_handler)
    app_logger.propagate = False  # prevent propagation to root

    # Set up the 'flats' logger
    flats_logger = logging.getLogger("flats")
    flats_logger.setLevel(logging.INFO)
    flats_logger.addHandler(flats_handler)
    flats_logger.propagate = False  # prevent propagation to root


