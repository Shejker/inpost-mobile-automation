import logging
from appium.webdriver.webdriver import WebDriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

logger = logging.getLogger(__name__)


class BasePage:
    """Base page object class for all page models.

    Provides common methods for element interaction and navigation.
    """

    def __init__(self, driver: WebDriver):
        """Initialize BasePage with Appium driver.

        Args:
            driver: Appium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait[WebDriver](driver, 20)

    def find_element(self, locator):
        """Find single element using explicit wait.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.

        Returns:
            WebElement if found.

        Raises:
            TimeoutException: If element not found within timeout.
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator):
        """Find multiple elements using explicit wait.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.

        Returns:
            List of WebElements if found.

        Raises:
            TimeoutException: If elements not found within timeout.
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            return elements
        except TimeoutException:
            logger.error(f"Elements not found: {locator}")
            raise

    def click(self, locator):
        """Click on element after waiting for it to be clickable.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def send_keys(self, locator, text):
        """Clear and send text to input element.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.
            text: Text to enter into the element.
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        """Get text content from element.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.

        Returns:
            Text content of the element.
        """
        element = self.find_element(locator)
        return element.text

    def is_displayed(self, locator, timeout=5):
        """Check if element is visible on screen.

        Args:
            locator: Tuple of (AppiumBy, value) for element localization.
            timeout: Wait timeout in seconds. Defaults to 5.

        Returns:
            True if element is visible, False otherwise.
        """
        try:
            wait = WebDriverWait[WebDriver](self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def scroll_to_text(self, text_to_find):
        """Scroll to element by text content (Android only).

        Args:
            text_to_find: Text to search for in scrollable container.

        Returns:
            WebElement at text location.
        """
        logger.info(f"Scrolling to text: {text_to_find}")

        android_uiautomator = (
            f"new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().text("{text_to_find}"))'
        )

        element = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, android_uiautomator
        )
        return element

    def scroll_to_accessibility_id(self, accessibility_id):
        """Scroll to element by accessibility ID (Android only).

        Args:
            accessibility_id: Accessibility ID to search for.

        Returns:
            WebElement at accessibility ID location.
        """
        logger.info(f"Scrolling to element: {accessibility_id}")

        android_uiautomator = (
            f"new UiScrollable(new UiSelector().scrollable(true))"
            f'.scrollIntoView(new UiSelector().description("{accessibility_id}"))'
        )

        element = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, android_uiautomator
        )
        return element
