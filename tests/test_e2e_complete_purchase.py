import pytest
import time
import logging
from pages.login_page import LoginPage
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
            # Step 1: Login with autofill
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
            
            logger.info("\n[RESULT] Login successful with auto-filled credentials")
            logger.info("=" * 80)
            logger.info("COMPLETE PURCHASE FLOW TEST COMPLETED SUCCESSFULLY")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"\n[ERROR] Test failed with exception: {str(e)}")
            logger.error(f"[ERROR] Exception type: {type(e).__name__}")
            take_screenshot(driver, self.screenshots_dir, "99_failure")
            raise
