import logging
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler

def setup_loggers():
    Path("logs").mkdir(exist_ok=True)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # Timed rotation for app.log: every 7 days
    app_handler = TimedRotatingFileHandler(
        "logs/app.log",
        when="d",
        interval=7,
        backupCount=30,
        encoding="utf-8"
    )
    app_handler.setFormatter(formatter)

    # Timed rotation for flats.log: every 7 days
    flats_handler = TimedRotatingFileHandler(
        "logs/flats.log",
        when="d",
        interval=7,
        backupCount=30,
        encoding="utf-8"
    )
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


