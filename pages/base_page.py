import logging
import time
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    def find_element(self, locator):
        logger.info(f"Finding element: {locator}")
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            logger.info(f"Element found: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator):
        logger.info(f"Finding elements: {locator}")
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            raise

    def click(self, locator):
        logger.info(f"Clicking element: {locator}")
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        logger.info(f"Clicked element: {locator}")

    def send_keys(self, locator, text):
        logger.info(f"Sending keys to {locator}: {text}")
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        logger.info(f"Sent keys to {locator}")

    def get_text(self, locator):
        logger.info(f"Getting text from: {locator}")
        element = self.find_element(locator)
        text = element.text
        logger.info(f"Got text: {text}")
        return text

    def is_displayed(self, locator, timeout=5):
        logger.info(f"Checking if displayed: {locator}")
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            logger.info(f"Element is displayed: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element not displayed: {locator}")
            return False

    def scroll_to_text(self, text_to_find):
        logger.info(f"Scrolling to text: {text_to_find}")
        
        android_uiautomator = (
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text_to_find}"))'
        )
        
        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, android_uiautomator)
        logger.info(f"Scrolled to text: {text_to_find}")
        return element
    
    def scroll_to_accessibility_id(self, accessibility_id):
        logger.info(f"Scrolling to element with id: {accessibility_id}")
        
        android_uiautomator = (
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().description("{accessibility_id}"))'
        )
        
        element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, android_uiautomator)
        logger.info(f"Scrolled to element: {accessibility_id}")
        return element
