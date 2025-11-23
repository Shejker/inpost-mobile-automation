"""
Example fixtures for different platforms and devices.
Use these as templates for setting up tests on iOS, emulators, etc.
"""

import pytest
from appium import webdriver
from pathlib import Path
import logging

from config.capabilities import (
    get_android_emulator_capabilities,
    get_ios_capabilities,
    get_ios_simulator_capabilities,
)

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def android_emulator_driver(request):
    """Android emulator fixture"""
    logger.info("Setting up Android emulator driver")

    app_path = Path(__file__).parent.parent / "builds/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk"

    options = get_android_emulator_capabilities(str(app_path.absolute()))

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def ios_device_driver(request):
    """iOS physical device fixture"""
    logger.info("Setting up iOS physical device driver")

    app_path = Path(__file__).parent.parent / "builds/SauceLabs-iOS.ipa"

    options = get_ios_capabilities(udid="<your_ios_udid>", app_path=str(app_path.absolute()))

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def ios_simulator_driver(request):
    """iOS simulator fixture"""
    logger.info("Setting up iOS simulator driver")

    app_path = Path(__file__).parent.parent / "builds/SauceLabs-iOS.ipa"

    options = get_ios_simulator_capabilities(str(app_path.absolute()))

    driver = webdriver.Remote("http://localhost:4723", options=options)
    yield driver
    driver.quit()
