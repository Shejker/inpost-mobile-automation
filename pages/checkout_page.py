import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutPage(BasePage):
    """Checkout information page object model.

    Handles shipping and billing information collection.
    """

    CHECKOUT_INFORMATION_TITLE = (
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().text("CHECKOUT: INFORMATION")',
    )
    FIRST_NAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-First Name")
    LAST_NAME_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Last Name")
    ZIP_CODE_INPUT = (AppiumBy.ACCESSIBILITY_ID, "test-Zip/Postal Code")
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CONTINUE")
    ERROR_MESSAGE = (AppiumBy.ACCESSIBILITY_ID, "test-Error message")

    def fill_checkout_information(self, first_name, last_name, zip_code):
        """Fill shipping information form.

        Args:
            first_name: Customer first name.
            last_name: Customer last name.
            zip_code: Postal/ZIP code.
        """
        self.send_keys(self.FIRST_NAME_INPUT, first_name)
        self.send_keys(self.LAST_NAME_INPUT, last_name)
        self.send_keys(self.ZIP_CODE_INPUT, zip_code)
        logger.info(f"Checkout information filled: {first_name} {last_name} {zip_code}")

    def click_continue(self):
        """Click continue button to proceed to checkout overview."""
        self.click(self.CONTINUE_BUTTON)

    def verify_no_error_after_continue(self):
        """Verify no validation errors appeared after clicking continue.

        Raises:
            AssertionError: If validation error is displayed.
        """
        has_error = self.is_displayed(self.ERROR_MESSAGE, timeout=2)
        if has_error:
            raise AssertionError("Validation error appeared - invalid checkout data")
        logger.info("Checkout data accepted")
