import pytest
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.helpers import take_screenshot

logger = logging.getLogger(__name__)


@pytest.mark.android
@pytest.mark.smoke
class TestLoginFormValidation:
    screenshots_dir = None

    def test_login_empty_username_empty_password(self, driver):
        logger.info("Test: Empty username and empty password")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)
        take_screenshot(driver, self.screenshots_dir, "01_login_screen")

        logger.info("  - Clicking LOGIN with empty fields...")
        login_page.click_login()

        logger.info("  - Verifying error message...")
        login_page.find_element(login_page.ERROR_MESSAGE)
        logger.info("  [OK] Error message displayed for empty fields")
        take_screenshot(driver, self.screenshots_dir, "02_error_empty_both")

    def test_login_empty_password_filled_username(self, driver):
        logger.info("Test: Filled username and empty password")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Scrolling to username field...")
        login_page.scroll_to_accessibility_id("test-Username")

        logger.info("  - Filling username field...")
        login_page.send_keys(login_page.USERNAME_INPUT, "standard_user")
        logger.info("  [OK] Username filled")

        logger.info("  - Scrolling to LOGIN button...")
        login_page.scroll_to_accessibility_id("test-LOGIN")
        take_screenshot(driver, self.screenshots_dir, "01_filled_username")

        logger.info("  - Clicking LOGIN with empty password...")
        login_page.click_login()

        logger.info("  - Verifying error message...")
        login_page.find_element(login_page.ERROR_MESSAGE)
        logger.info("  [OK] Error message displayed for empty password")
        take_screenshot(driver, self.screenshots_dir, "02_error_empty_password")

    def test_login_empty_username_filled_password(self, driver):
        logger.info("Test: Empty username and filled password")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Scrolling to password field...")
        login_page.scroll_to_accessibility_id("test-Password")

        logger.info("  - Filling password field...")
        login_page.send_keys(login_page.PASSWORD_INPUT, "password123")
        logger.info("  [OK] Password filled")
        take_screenshot(driver, self.screenshots_dir, "01_filled_password")

        logger.info("  - Scrolling to LOGIN button...")
        login_page.scroll_to_accessibility_id("test-LOGIN")

        logger.info("  - Clicking LOGIN with empty username...")
        login_page.click_login()

        logger.info("  - Verifying error message...")
        login_page.find_element(login_page.ERROR_MESSAGE)
        logger.info("  [OK] Error message displayed for empty username")
        take_screenshot(driver, self.screenshots_dir, "02_error_empty_username")


@pytest.mark.android
@pytest.mark.smoke
class TestCheckoutFormValidation:
    screenshots_dir = None

    def test_checkout_all_fields_empty(self, driver):
        logger.info("Test: All checkout fields empty")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Login with standard_user...")
        login_page.scroll_to_standard_user()
        login_page.select_standard_user()
        login_page.scroll_to_accessibility_id("test-LOGIN")
        login_page.click_login()
        login_page.wait_for_products_page()
        logger.info("  [OK] Logged in")

        products_page = ProductsPage(driver)
        logger.info("  - Adding random product to cart...")
        products_page.add_random_product_to_cart()
        logger.info("  [OK] Product added")
        take_screenshot(driver, self.screenshots_dir, "01_product_added")

        logger.info("  - Opening cart...")
        cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
        cart_icon.click()
        logger.info("  [OK] Cart opened")

        cart_page = CartPage(driver)
        logger.info("  - Clicking checkout...")
        cart_page.click_checkout()
        logger.info("  [OK] Checkout clicked")

        checkout_page = CheckoutPage(driver)
        logger.info("  - Clicking CONTINUE with empty fields...")
        checkout_page.click_continue()

        logger.info("  - Verifying error message...")
        has_error = checkout_page.is_displayed(checkout_page.ERROR_MESSAGE, timeout=2)
        assert has_error, "Error message should be displayed"
        logger.info("  [OK] Error message displayed for empty fields")
        take_screenshot(driver, self.screenshots_dir, "02_error_all_empty")

    def test_checkout_empty_first_name(self, driver):
        logger.info("Test: Empty first name, filled last name and zip code")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Login with standard_user...")
        login_page.scroll_to_standard_user()
        login_page.select_standard_user()
        login_page.scroll_to_accessibility_id("test-LOGIN")
        login_page.click_login()
        login_page.wait_for_products_page()

        products_page = ProductsPage(driver)
        logger.info("  - Adding random product to cart...")
        products_page.add_random_product_to_cart()
        logger.info("  [OK] Product added")
        take_screenshot(driver, self.screenshots_dir, "01_product_added")

        logger.info("  - Opening cart...")
        cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
        cart_icon.click()
        logger.info("  [OK] Cart opened")

        cart_page = CartPage(driver)
        logger.info("  - Clicking checkout...")
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        logger.info("  - Filling only last name and zip code...")
        checkout_page.send_keys(checkout_page.LAST_NAME_INPUT, "Doe")
        checkout_page.send_keys(checkout_page.ZIP_CODE_INPUT, "12345")
        logger.info("  [OK] Filled last name and zip code")
        take_screenshot(driver, self.screenshots_dir, "01_empty_first_name")

        logger.info("  - Clicking CONTINUE...")
        checkout_page.click_continue()

        logger.info("  - Verifying error message...")
        has_error = checkout_page.is_displayed(checkout_page.ERROR_MESSAGE, timeout=2)
        assert has_error, "Error message should be displayed"
        logger.info("  [OK] Error message displayed for empty first name")
        take_screenshot(driver, self.screenshots_dir, "02_error_first_name")

    def test_checkout_empty_last_name(self, driver):
        logger.info("Test: Filled first name and zip code, empty last name")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Login with standard_user...")
        login_page.scroll_to_standard_user()
        login_page.select_standard_user()
        login_page.scroll_to_accessibility_id("test-LOGIN")
        login_page.click_login()
        login_page.wait_for_products_page()

        products_page = ProductsPage(driver)
        logger.info("  - Adding random product to cart...")
        products_page.add_random_product_to_cart()
        logger.info("  [OK] Product added")
        take_screenshot(driver, self.screenshots_dir, "01_product_added")

        logger.info("  - Opening cart...")
        cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
        cart_icon.click()
        logger.info("  [OK] Cart opened")

        cart_page = CartPage(driver)
        logger.info("  - Clicking checkout...")
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        logger.info("  - Filling first name and zip code...")
        checkout_page.send_keys(checkout_page.FIRST_NAME_INPUT, "John")
        checkout_page.send_keys(checkout_page.ZIP_CODE_INPUT, "12345")
        logger.info("  [OK] Filled first name and zip code")
        take_screenshot(driver, self.screenshots_dir, "01_empty_last_name")

        logger.info("  - Clicking CONTINUE...")
        checkout_page.click_continue()

        logger.info("  - Verifying error message...")
        has_error = checkout_page.is_displayed(checkout_page.ERROR_MESSAGE, timeout=2)
        assert has_error, "Error message should be displayed"
        logger.info("  [OK] Error message displayed for empty last name")
        take_screenshot(driver, self.screenshots_dir, "02_error_last_name")

    def test_checkout_empty_zip_code(self, driver):
        logger.info("Test: Filled first name and last name, empty zip code")

        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Login with standard_user...")
        login_page.scroll_to_standard_user()
        login_page.select_standard_user()
        login_page.scroll_to_accessibility_id("test-LOGIN")
        login_page.click_login()
        login_page.wait_for_products_page()

        products_page = ProductsPage(driver)
        logger.info("  - Adding random product to cart...")
        products_page.add_random_product_to_cart()
        logger.info("  [OK] Product added")
        take_screenshot(driver, self.screenshots_dir, "01_product_added")

        logger.info("  - Opening cart...")
        cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
        cart_icon.click()
        logger.info("  [OK] Cart opened")

        cart_page = CartPage(driver)
        logger.info("  - Clicking checkout...")
        cart_page.click_checkout()

        checkout_page = CheckoutPage(driver)
        logger.info("  - Filling first name and last name...")
        checkout_page.send_keys(checkout_page.FIRST_NAME_INPUT, "John")
        checkout_page.send_keys(checkout_page.LAST_NAME_INPUT, "Doe")
        logger.info("  [OK] Filled first name and last name")
        take_screenshot(driver, self.screenshots_dir, "01_empty_zip_code")

        logger.info("  - Clicking CONTINUE...")
        checkout_page.click_continue()

        logger.info("  - Verifying error message...")
        has_error = checkout_page.is_displayed(checkout_page.ERROR_MESSAGE, timeout=2)
        assert has_error, "Error message should be displayed"
        logger.info("  [OK] Error message displayed for empty zip code")
        take_screenshot(driver, self.screenshots_dir, "02_error_zip_code")
