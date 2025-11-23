import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page object model.

    Handles user authentication and login flow.
    """

    USERNAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Username")
    PASSWORD_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Password")
    LOGIN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")
    PRODUCTS_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("PRODUCTS")',
    )
    ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")
    STANDARD_USER_TEXT = "standard_user"

    def scroll_to_standard_user(self):
        """Scroll to standard_user option in dropdown."""
        logger.info("Scrolling to standard_user option")
        self.scroll_to_text(self.STANDARD_USER_TEXT)

    def select_standard_user(self):
        """Click on standard_user option."""
        logger.info("Clicking on standard_user option")
        element = self.scroll_to_text(self.STANDARD_USER_TEXT)
        element.click()
        logger.info("Clicked on standard_user")

    def get_username_value(self):
        """Get username value from input field.

        Returns:
            Username string or "EMPTY" if not set.
        """
        logger.info("Getting username value")
        element = self.find_element(self.USERNAME_INPUT)

        username = element.text or element.get_attribute("text") or "EMPTY"
        logger.info(f"Username value: {username}")
        return username

    def click_login(self):
        """Click login button to authenticate."""
        logger.info("Clicking LOGIN button")
        self.click(self.LOGIN_BUTTON)
        logger.info("Clicked LOGIN button")

    def wait_for_products_page(self):
        """Wait for products page to load after login."""
        logger.info("Waiting for PRODUCTS page to load")
        self.find_element(self.PRODUCTS_TITLE)
        logger.info("PRODUCTS page loaded")

    def login_with_standard_user(self):
        """Complete login flow with standard_user.

        Raises:
            AssertionError: If username not properly selected.
        """
        logger.info("=== Starting login with standard_user ===")
        self.scroll_to_standard_user()
        self.select_standard_user()
        username = self.get_username_value()
        assert username == "standard_user", (
            f"Expected 'standard_user', got '{username}'"
        )
        self.click_login()
        logger.info("=== Login completed ===")
