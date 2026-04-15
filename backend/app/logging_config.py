import logging
import sys

def setup_logging():
    # Define logging format
    logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=logging_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            # Optional: Add FileHandler here for persistence
            # logging.FileHandler("app.log")
        ]
    )

    # Specific logger for our app
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)
    
    return logger
