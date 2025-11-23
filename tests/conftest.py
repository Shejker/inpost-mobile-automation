import sys
import logging
import pytest
from pathlib import Path
from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options

sys.path.insert(0, str(Path(__file__).parent.parent))

from config import settings

results_dir = Path(__file__).parent.parent / "results"
results_dir.mkdir(exist_ok=True)

logs_dir = results_dir / "logs"
logs_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(logs_dir / "appium.log"), logging.StreamHandler()],
)


@pytest.fixture(scope="function")
def driver(request):
    logger = logging.getLogger(__name__)

    logger.info("=" * 80)
    logger.info("APPIUM DRIVER SETUP")
    logger.info("=" * 80)
    logger.info(f"Appium Server: {settings.APPIUM_SERVER}")
    logger.info(f"Device UDID: {settings.UDID if settings.UDID else 'Auto-detected'}")
    logger.info(
        f"Platform Version: {settings.PLATFORM_VERSION if settings.PLATFORM_VERSION else 'Auto-detected'}"
    )
    logger.info(f"App Path: {settings.APP_PATH}")
    logger.info(f"App Package: {settings.APP_PACKAGE}")
    logger.info(f"App Activity: {settings.APP_ACTIVITY}")
    logger.info(f"Full Reset: {settings.FULL_RESET}")
    logger.info("=" * 80)

    app_path = Path(__file__).parent.parent / settings.APP_PATH

    test_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    test_results_dir = results_dir / test_timestamp
    test_results_dir.mkdir(exist_ok=True)

    screenshots_dir = test_results_dir / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    if hasattr(request, "instance") and request.instance is not None:
        request.instance.screenshots_dir = screenshots_dir

    options = UiAutomator2Options()
    if settings.PLATFORM_VERSION:
        options.platform_version = settings.PLATFORM_VERSION
    options.udid = settings.UDID
    options.app = str(app_path.absolute())
    options.full_reset = settings.FULL_RESET
    options.app_package = settings.APP_PACKAGE
    options.app_activity = settings.APP_ACTIVITY
    options.app_wait_duration = 30000

    android_driver = webdriver.Remote(settings.APPIUM_SERVER, options=options)
    yield android_driver
    android_driver.quit()
