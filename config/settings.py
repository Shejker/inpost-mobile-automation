import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

APPIUM_SERVER = os.getenv('APPIUM_SERVER', 'http://localhost:4723')
PLATFORM_VERSION = os.getenv('PLATFORM_VERSION')
UDID = os.getenv('UDID')
APP_PATH = os.getenv('APP_PATH')
APP_PACKAGE = os.getenv('APP_PACKAGE')
APP_ACTIVITY = os.getenv('APP_ACTIVITY')
FULL_RESET = os.getenv('FULL_RESET', 'false').lower() == 'true'
