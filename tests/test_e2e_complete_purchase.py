import pytest
import time
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.checkout_overview_page import CheckoutOverviewPage
from utils.helpers import take_screenshot

logger = logging.getLogger(__name__)


@pytest.mark.android
@pytest.mark.smoke
class TestCompletePurchaseFlow:
    
    def test_complete_purchase_with_autofill_login(self, driver):
        """
        Complete purchase flow:
        1. Login with standard_user autofill
        2. Add product to cart
        3. Open shopping cart
        4. Continue to checkout
        5. Fill checkout information
        6. Proceed to payment
        7. Fill payment information
        8. Review order
        9. Place order and complete purchase
        """
        logger.info("=" * 80)
        logger.info("STARTING COMPLETE PURCHASE FLOW TEST")
        logger.info("=" * 80)
        
        try:
            logger.info("\n[STEP 1] Login with standard_user autofill")
            login_page = LoginPage(driver)
            
            logger.info("  - Waiting for LOGIN button to appear...")
            login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)
            take_screenshot(driver, self.screenshots_dir, "01_application_opened")
            logger.info("  [OK] Application opened")
            
            logger.info("  - Scrolling to standard_user button...")
            login_page.scroll_to_standard_user()
            logger.info("  [OK] Scrolled to standard_user button")
            
            logger.info("  - Clicking standard_user to auto-fill credentials...")
            login_page.select_standard_user()
            logger.info("  [OK] Clicked standard_user")
            
            logger.info("  - Scrolling to LOGIN button...")
            login_page.scroll_to_accessibility_id('test-LOGIN')
            
            logger.info("  - Verifying username auto-fill...")
            username = login_page.get_username_value()
            assert username == 'standard_user', f"Expected 'standard_user', got '{username}'"
            logger.info(f"  [OK] Username auto-filled correctly: {username}")
            take_screenshot(driver, self.screenshots_dir, "02_credentials_filled")
            
            logger.info("  - Clicking LOGIN button...")
            login_page.click_login()
            logger.info("  [OK] LOGIN button clicked")
            
            logger.info("  - Waiting for PRODUCTS page to load...")
            login_page.wait_for_products_page()
            take_screenshot(driver, self.screenshots_dir, "03_logged_in")
            logger.info("  [OK] PRODUCTS page loaded - login confirmed")
            
            logger.info("\n[STEP 2] Add random product to cart")
            products_page = ProductsPage(driver)
            
            logger.info("  - Selecting and adding random product...")
            product = products_page.add_random_product_to_cart()
            logger.info(f"  [OK] Added {product['name']} ({product['price']}) to cart")
            take_screenshot(driver, self.screenshots_dir, "04_product_added")
            
            logger.info("\n[STEP 3] Open cart and verify product")
            logger.info("  - Opening cart...")
            cart_icon = products_page.find_element((AppiumBy.ACCESSIBILITY_ID, "test-Cart"))
            cart_icon.click()
            logger.info("  [OK] Cart opened")
            
            logger.info("  - Verifying product in cart...")
            cart_page = CartPage(driver)
            cart_page.verify_product_in_cart(product['name'], product['price'])
            logger.info(f"  [OK] Product {product['name']} ({product['price']}) verified in cart")
            take_screenshot(driver, self.screenshots_dir, "05_cart_opened")
            
            logger.info("  - Clicking CHECKOUT...")
            cart_page.click_checkout()
            logger.info("  [OK] CHECKOUT clicked")
            take_screenshot(driver, self.screenshots_dir, "06_checkout_button_clicked")
            
            logger.info("\n[STEP 4] Fill checkout information")
            checkout_page = CheckoutPage(driver)
            
            logger.info("  - Filling checkout form...")
            checkout_page.fill_checkout_information("John", "Doe", "12345")
            logger.info("  [OK] Checkout form filled")
            take_screenshot(driver, self.screenshots_dir, "07_checkout_filled")
            
            logger.info("  - Clicking CONTINUE...")
            checkout_page.click_continue()
            logger.info("  [OK] CONTINUE clicked")
            
            logger.info("  - Verifying no validation errors...")
            checkout_page.verify_no_error_after_continue()
            logger.info("  [OK] Data accepted")
            
            logger.info("\n[STEP 5] Verify checkout overview page")
            checkout_overview_page = CheckoutOverviewPage(driver)
            checkout_overview_page.verify_checkout_overview_page()
            logger.info("  [OK] On checkout overview page")
            
            logger.info(f"  - Verifying product in overview: {product['name']}")
            checkout_overview_page.verify_product_in_overview(product['name'], product['price'])
            logger.info(f"  [OK] Product '{product['name']}' ({product['price']}) confirmed in overview")
            take_screenshot(driver, self.screenshots_dir, "08_checkout_overview")
            
            logger.info("  - Clicking FINISH to complete purchase...")
            checkout_overview_page.click_finish()
            logger.info("  [OK] FINISH clicked")
            
            logger.info("  - Verifying purchase complete page...")
            checkout_overview_page.verify_purchase_complete()
            logger.info("  [OK] Purchase complete verified")
            take_screenshot(driver, self.screenshots_dir, "09_purchase_complete")
            
            logger.info("\n[STEP 6] Return to products page")
            logger.info("  - Clicking BACK HOME...")
            checkout_overview_page.click_back_home()
            logger.info("  [OK] BACK HOME clicked")
            
            logger.info("  - Verifying products page loaded...")
            products_page_return = ProductsPage(driver)
            products_page_return.find_element(LoginPage.PRODUCTS_TITLE)
            logger.info("  [OK] Back on products page")
            take_screenshot(driver, self.screenshots_dir, "10_back_home")
            
            logger.info("\n[RESULT] Complete purchase flow successful!")
            logger.info("=" * 80)
            logger.info("TEST COMPLETE: Purchase finished successfully and returned home")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"\n[ERROR] Test failed with exception: {str(e)}")
            logger.error(f"[ERROR] Exception type: {type(e).__name__}")
            take_screenshot(driver, self.screenshots_dir, "99_failure")
            raise
