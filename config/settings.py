import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = BASE_DIR / '.env'
if env_path.exists():
    load_dotenv(env_path)

PLATFORM_NAME = os.getenv('PLATFORM_NAME', 'Android')
PLATFORM_VERSION = os.getenv('PLATFORM_VERSION', '13')
DEVICE_NAME = os.getenv('DEVICE_NAME', '')
UDID = os.getenv('UDID', '')
APP_PACKAGE = os.getenv('APP_PACKAGE', '')
APP_ACTIVITY = os.getenv('APP_ACTIVITY', '')
APPIUM_SERVER = os.getenv('APPIUM_SERVER', 'http://localhost:4723')