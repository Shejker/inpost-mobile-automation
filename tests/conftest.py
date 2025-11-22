import sys
import logging
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))

results_dir = Path(__file__).parent.parent / 'results'
results_dir.mkdir(exist_ok=True)

logs_dir = results_dir / 'logs'
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(logs_dir / 'appium.log'),
        logging.StreamHandler()
    ]
)

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config import settings


@pytest.fixture(scope='function')
def driver(request):
    app_path = Path(__file__).parent.parent / settings.APP_PATH
    
    test_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    test_results_dir = results_dir / test_timestamp
    test_results_dir.mkdir(exist_ok=True)
    
    screenshots_dir = test_results_dir / 'screenshots'
    screenshots_dir.mkdir(exist_ok=True)
    
    if hasattr(request, 'instance') and request.instance is not None:
        request.instance.screenshots_dir = screenshots_dir
    
    options = UiAutomator2Options()
    options.udid = settings.UDID
    options.app = str(app_path.absolute())
    options.full_reset = settings.FULL_RESET
    options.app_package = settings.APP_PACKAGE
    options.app_activity = settings.APP_ACTIVITY
    options.app_wait_duration = 30000
    
    android_driver = webdriver.Remote(settings.APPIUM_SERVER, options=options)
    yield android_driver
    android_driver.quit()
