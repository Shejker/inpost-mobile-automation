import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    CART_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("YOUR CART")')
    CHECKOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT")
    
    def verify_product_in_cart(self, product_name, product_price=None):
        xpath = f'//android.widget.TextView[@text="{product_name}"]'
        self.find_element((AppiumBy.XPATH, xpath))
        logger.info(f"Product '{product_name}' found in cart")
        
        if product_price:
            price_xpath = f'//android.widget.TextView[@text="{product_name}"]/ancestor::android.view.ViewGroup//android.widget.TextView[@text="{product_price}"]'
            self.find_element((AppiumBy.XPATH, price_xpath))
            logger.info(f"Price verified in cart: {product_price}")
    
    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
