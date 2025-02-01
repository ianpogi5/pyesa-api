import os
import uvicorn
from uvicorn.config import LOGGING_CONFIG
from dotenv import load_dotenv

load_dotenv()

LOG_NAME = os.environ.get("LOG_NAME", "pyesa-api")
LOG_MAX_BYTES = int(os.environ.get("LOG_MAX_BYTES", 10000000))  # 10MB
LOG_BACKUP_COUNT = int(os.environ.get("LOG_BACKUP_COUNT", 10))
LOG_FORMAT = "%(asctime)s :: %(levelname)s :: %(message)s"
API_LOG_LEVEL = os.environ.get("API_LOG_LEVEL", "info")
API_PORT = int(os.environ.get("API_PORT", 8000))

if __name__ == "__main__":
    # Setup config
    log_file_path = os.environ.get(
        "LOG_PATH",
        f"logs/{LOG_NAME}.log",
    )

    LOGGING_CONFIG["handlers"]["file"] = {
        "class": "logging.handlers.RotatingFileHandler",
        "filename": log_file_path,
        "formatter": "default",
        "maxBytes": LOG_MAX_BYTES,
        "backupCount": LOG_BACKUP_COUNT,
    }
    LOGGING_CONFIG["loggers"]["uvicorn"]["handlers"] = ["default", "file"]
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = LOG_FORMAT

    # Run API server
    uvicorn.run(
        "app:app",
        app_dir=f"{os.path.dirname(__file__)}",
        host="0.0.0.0",
        port=API_PORT,
        log_level=API_LOG_LEVEL,
    )
