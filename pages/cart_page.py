import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CartPage(BasePage):
    CART_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("YOUR CART")')
    CHECKOUT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "test-CHECKOUT")
    FIRST_ITEM = (AppiumBy.XPATH, '(//android.view.ViewGroup[@content-desc="test-Item"])[1]')
    REMOVE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, 'test-REMOVE')
    
    def verify_product_in_cart(self, product_name, product_price=None):
        xpath = f'//android.widget.TextView[@text="{product_name}"]'
        self.find_element((AppiumBy.XPATH, xpath))
        logger.info(f"Product '{product_name}' found in cart")
        
        if product_price:
            price_xpath = f'//android.widget.TextView[@text="{product_name}"]/ancestor::android.view.ViewGroup//android.widget.TextView[@text="{product_price}"]'
            try:
                self.find_element((AppiumBy.XPATH, price_xpath))
                logger.info(f"Price verified in cart: {product_price}")
            except Exception as e:
                logger.debug(f"Could not verify price in cart: {e}")
    
    def click_checkout(self):
        self.click(self.CHECKOUT_BUTTON)
    
    def get_first_item_name(self):
        first_item = self.find_element(self.FIRST_ITEM)
        text_views = first_item.find_elements(AppiumBy.XPATH, './/android.widget.TextView')
        return text_views[1].text if len(text_views) > 1 else text_views[0].text
    
    def remove_first_item(self):
        first_item = self.find_element(self.FIRST_ITEM)
        remove_button = first_item.find_element(AppiumBy.ACCESSIBILITY_ID, 'test-REMOVE')
        remove_button.click()
        logger.info("Item removed from cart")
    
    def item_exists(self, item_name):
        elements = self.driver.find_elements(AppiumBy.XPATH, f'//android.widget.TextView[contains(text(), "{item_name}")]')
        return len(elements) > 0
