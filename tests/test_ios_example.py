"""
Example test for iOS platform.
This demonstrates how to write tests compatible with iOS devices/simulators.

To use: Replace conftest.py fixture with one from conftest_examples.py
"""

import pytest
import logging
from appium.webdriver.common.appiumby import AppiumBy

logger = logging.getLogger(__name__)


@pytest.mark.ios
@pytest.mark.skip(reason="iOS test example - requires iOS app")
class TestiOSExample:
    """Example iOS tests"""

    def test_ios_login(self, ios_device_driver):
        """Example: Login on iOS device"""
        logger.info("Test: iOS Login")

        driver = ios_device_driver

        # iOS uses different selectors than Android
        # XPath: //XCUIElementTypeTextField
        # Predicate: type == "XCUIElementTypeSecureTextField"

        username_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeTextField[@name='username']")
        username_field.send_keys("standard_user")

        password_field = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeSecureTextField[@name='password']")
        password_field.send_keys("password123")

        login_button = driver.find_element(AppiumBy.XPATH, "//XCUIElementTypeButton[@name='LOGIN']")
        login_button.click()

        logger.info("[OK] iOS login successful")
