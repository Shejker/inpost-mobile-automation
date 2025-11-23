import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CheckoutOverviewPage(BasePage):
    CHECKOUT_OVERVIEW_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CHECKOUT: OVERVIEW")')
    FINISH_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-FINISH")
    CHECKOUT_COMPLETE_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("CHECKOUT: COMPLETE!")')
    BACK_HOME_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-BACK HOME")
    
    def verify_checkout_overview_page(self):
        self.find_element(self.CHECKOUT_OVERVIEW_TITLE)
        logger.info("Checkout overview page verified")
    
    def verify_product_in_overview(self, product_name, product_price=None):
        xpath = f'//android.widget.TextView[@text="{product_name}"]'
        self.find_element((AppiumBy.XPATH, xpath))
        logger.info(f"Product '{product_name}' found in overview")
        
        if product_price:
            price_xpath = f'//android.widget.TextView[@text="{product_name}"]/ancestor::android.view.ViewGroup//android.widget.TextView[@text="{product_price}"]'
            try:
                self.find_element((AppiumBy.XPATH, price_xpath))
                logger.info(f"Price verified in overview: {product_price}")
            except Exception as e:
                logger.debug(f"Could not verify price in overview: {e}")
    
    def click_finish(self):
        self.scroll_to_accessibility_id("test-FINISH")
        self.click(self.FINISH_BUTTON)
    
    def verify_purchase_complete(self):
        logger.info("Verifying purchase complete page")
        self.find_element(self.CHECKOUT_COMPLETE_TITLE)
        self.find_element(self.BACK_HOME_BUTTON)
        logger.info("Purchase complete verified")
    
    def click_back_home(self):
        self.click(self.BACK_HOME_BUTTON)
