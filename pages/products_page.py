import logging
import random
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ProductsPage(BasePage):
    PRODUCTS_TITLE = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("PRODUCTS")')
    PRODUCT_ITEMS = (
        AppiumBy.XPATH,
        '//android.view.ViewGroup[@content-desc="test-Item"]',
    )

    PRODUCTS = {
        "backpack": "Sauce Labs Backpack",
        "bike_light": "Sauce Labs Bike Light",
        "bolt_tshirt": "Sauce Labs Bolt T-Shirt",
        "fleece_jacket": "Sauce Labs Fleece Jacket",
        "onesie": "Sauce Labs Onesie",
        "tshirt_red": "Test.allTheThings() T-Shirt (Red)",
    }

    def get_random_product(self):
        product_key = random.choice(list(self.PRODUCTS.keys()))
        logger.info(f"Randomly selected product: {product_key}")
        return product_key

    def get_all_products(self):
        products = []
        collected_product_names = set()
        max_scroll_attempts = 10
        scroll_attempts = 0

        while scroll_attempts < max_scroll_attempts:
            items = self.find_elements(self.PRODUCT_ITEMS)

            items_added_this_round = False

            for index, item in enumerate(items):
                try:
                    name_element = item.find_element(
                        AppiumBy.XPATH,
                        './/android.widget.TextView[@content-desc="test-Item title"]',
                    )
                    price_element = item.find_element(
                        AppiumBy.XPATH,
                        './/android.widget.TextView[@content-desc="test-Price"]',
                    )

                    name = name_element.text
                    price = price_element.text

                    if name not in collected_product_names:
                        products.append({"name": name, "price": price})
                        collected_product_names.add(name)
                        items_added_this_round = True
                        logger.info(f"Product {len(products)}: {name} - {price}")
                except Exception as e:
                    logger.debug(f"Could not get product details: {e}")

            if items_added_this_round or scroll_attempts == 0:
                self.driver.swipe(
                    start_x=500, start_y=400, end_x=500, end_y=200, duration=500
                )
                scroll_attempts += 1
            else:
                break

        logger.info(f"Total products: {len(products)}")
        return products

    def add_product_to_cart_by_name(self, product_name):
        logger.info(f"Adding product: {product_name}")

        self.scroll_to_text(product_name)
        logger.info(f"Scrolled to {product_name}")

        all_products = self.find_elements(self.PRODUCT_ITEMS)
        product_index = None

        for index, product in enumerate(all_products, start=1):
            try:
                name_element = product.find_element(
                    AppiumBy.XPATH,
                    './/android.widget.TextView[@content-desc="test-Item title"]',
                )
                if name_element.text == product_name:
                    product_index = index
                    logger.info(f"Found {product_name} at index {product_index}")
                    break
            except Exception:
                continue

        if product_index is None:
            raise Exception(f"Could not find product {product_name} in visible items")

        max_swipe_attempts = 5
        price = None
        add_to_cart_button = None

        price_xpath = f'(//android.view.ViewGroup[@content-desc="test-Item"])[{product_index}]//android.widget.TextView[@content-desc="test-Price"]'
        add_to_cart_xpath = (
            f'(//android.widget.TextView[@text="ADD TO CART"])[{product_index}]'
        )

        for attempt in range(max_swipe_attempts):
            try:
                from selenium.webdriver.support.ui import WebDriverWait

                wait_short = WebDriverWait(self.driver, 2)

                price_element = wait_short.until(
                    lambda d: d.find_element(AppiumBy.XPATH, price_xpath)
                )
                price = price_element.text
                logger.info(f"Price: {price}")

                add_to_cart_button = wait_short.until(
                    lambda d: d.find_element(AppiumBy.XPATH, add_to_cart_xpath)
                )
                logger.info("ADD TO CART button found and visible")
                break
            except Exception:
                if attempt < max_swipe_attempts - 1:
                    logger.info(f"Price or button not visible, attempt {attempt + 1}")
                    self.driver.swipe(
                        start_x=500, start_y=700, end_x=500, end_y=300, duration=500
                    )
                else:
                    raise Exception(
                        f"Could not find price or button for {product_name}"
                    )

        add_to_cart_button.click()
        logger.info(f"Clicked ADD TO CART for {product_name}")

        logger.info(f"Successfully added {product_name} ({price}) to cart")
        return {"name": product_name, "price": price}

    def add_random_product_to_cart(self):
        product_key = self.get_random_product()
        product_name = self.PRODUCTS[product_key]
        return self.add_product_to_cart_by_name(product_name)

    def open_filters(self):
        filter_button = self.find_element(
            (AppiumBy.ACCESSIBILITY_ID, "test-Modal Selector Button")
        )
        filter_button.click()
        logger.info("Filters opened")

    def select_filter(self, filter_name):
        filter_element = self.driver.find_element(
            AppiumBy.XPATH, f'//android.widget.TextView[@text="{filter_name}"]'
        )
        filter_element.click()
        logger.info(f"Filter '{filter_name}' selected")
