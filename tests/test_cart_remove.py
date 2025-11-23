import pytest
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from utils.helpers import take_screenshot

logger = logging.getLogger(__name__)


@pytest.mark.android
@pytest.mark.smoke
class TestCartRemove:
    screenshots_dir = None

    def test_remove_all_items_from_cart(self, driver):
        logger.info("Test: Remove all items from cart")

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
        logger.info("  - Adding products to cart...")
        products_added = 0

        while True:
            add_to_cart_buttons = driver.find_elements(
                AppiumBy.XPATH, '//android.widget.TextView[@text="ADD TO CART"]'
            )

            if not add_to_cart_buttons:
                driver.swipe(
                    start_x=500, start_y=700, end_x=500, end_y=300, duration=500
                )
                add_to_cart_buttons = driver.find_elements(
                    AppiumBy.XPATH, '//android.widget.TextView[@text="ADD TO CART"]'
                )
                if not add_to_cart_buttons:
                    break

            for i in range(len(add_to_cart_buttons)):
                try:
                    buttons = driver.find_elements(
                        AppiumBy.XPATH, '//android.widget.TextView[@text="ADD TO CART"]'
                    )
                    if i < len(buttons):
                        buttons[i].click()
                        products_added += 1
                        take_screenshot(
                            driver,
                            self.screenshots_dir,
                            f"01_product_{products_added}_added",
                        )
                except Exception as e:
                    logger.warning(f"Could not click button: {e}")
                    continue

            driver.swipe(start_x=500, start_y=700, end_x=500, end_y=300, duration=500)

        logger.info(f"  [OK] Added {products_added} products to cart")
        take_screenshot(driver, self.screenshots_dir, "01_all_products_added")

        logger.info("  - Opening cart...")
        cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
        cart_icon.click()
        logger.info("  [OK] Cart opened")
        take_screenshot(driver, self.screenshots_dir, "02_cart_opened")

        cart_page = CartPage(driver)
        logger.info(f"  - Removing {products_added} items...")
        removed_count = 0

        while removed_count < products_added:
            item_name = cart_page.get_first_item_name()
            logger.info(f"  - Removing item: {item_name}")

            cart_page.remove_first_item()

            assert not cart_page.item_exists(item_name), (
                f"Item '{item_name}' still in cart"
            )

            removed_count += 1
            logger.info(f"  [OK] Item {item_name} removed")
            take_screenshot(driver, self.screenshots_dir, f"03_removed_{removed_count}")

        logger.info("  [OK] All items removed")
        take_screenshot(driver, self.screenshots_dir, "04_cart_empty")

        logger.info(
            f"\n[RESULT] Successfully removed all {removed_count} items from cart"
        )
