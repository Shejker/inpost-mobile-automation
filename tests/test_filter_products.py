import pytest
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.helpers import take_screenshot

logger = logging.getLogger(__name__)


@pytest.mark.android
@pytest.mark.smoke
class TestFilterProducts:
    screenshots_dir = None

    def _login(self, driver):
        login_page = LoginPage(driver)
        login_page.is_displayed(login_page.LOGIN_BUTTON, timeout=10)

        logger.info("  - Login with standard_user...")
        login_page.scroll_to_standard_user()
        login_page.select_standard_user()
        login_page.scroll_to_accessibility_id("test-LOGIN")
        login_page.click_login()
        login_page.wait_for_products_page()
        logger.info("  [OK] Logged in")

    def _collect_products(self, driver, max_iterations=5):
        products = []
        iteration = 0

        while iteration < max_iterations:
            iteration += 1
            add_to_cart_buttons = driver.find_elements(
                AppiumBy.XPATH, '//android.widget.TextView[@text="ADD TO CART"]'
            )

            if not add_to_cart_buttons:
                logger.info("  [OK] No more products found")
                break

            items = driver.find_elements(
                AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="test-Item"]'
            )
            for item in items:
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

                    if not any(p["name"] == name for p in products):
                        products.append({"name": name, "price": price})
                        logger.info(f"  - Product {len(products)}: {name} - {price}")
                except Exception as e:
                    logger.debug(f"Could not get product details: {e}")

            logger.info("  - Swiping down for more products...")
            driver.swipe(start_x=500, start_y=700, end_x=500, end_y=300, duration=500)

        logger.info(f"  [OK] Retrieved {len(products)} products total")
        return products

    def _extract_price(self, price_str):
        return float(price_str.replace("$", "").strip())

    @pytest.mark.parametrize(
        "filter_name,sort_key,reverse",
        [
            ("Name (A to Z)", lambda x: x["name"], False),
            ("Name (Z to A)", lambda x: x["name"], True),
            (
                "Price (low to high)",
                lambda x: float(x["price"].replace("$", "").strip()),
                False,
            ),
            (
                "Price (high to low)",
                lambda x: float(x["price"].replace("$", "").strip()),
                True,
            ),
        ],
        ids=["name_a_to_z", "name_z_to_a", "price_low_to_high", "price_high_to_low"],
    )
    def test_filter_products(self, driver, filter_name, sort_key, reverse):
        logger.info(f"Test: Filter products by {filter_name}")

        self._login(driver)

        products_page = ProductsPage(driver)
        logger.info("  - Opening filters...")
        products_page.open_filters()
        take_screenshot(driver, self.screenshots_dir, "01_filters_opened")

        logger.info(f"  - Selecting {filter_name} filter...")
        products_page.select_filter(filter_name)
        take_screenshot(driver, self.screenshots_dir, "02_filter_selected")

        products = self._collect_products(driver)

        logger.info(f"  - Verifying products are sorted by {filter_name}...")
        sorted_products = sorted(products, key=sort_key, reverse=reverse)
        product_keys = [sort_key(p) for p in products]
        sorted_keys = [sort_key(p) for p in sorted_products]

        if isinstance(product_keys[0], float):
            for i, (actual, expected) in enumerate(zip(product_keys, sorted_keys)):
                assert abs(actual - expected) < 0.01, (
                    f"Product {i + 1} price mismatch: {actual} != {expected}"
                )
        else:
            assert product_keys == sorted_keys, (
                f"Products not sorted correctly. Got: {product_keys}, Expected: {sorted_keys}"
            )

        logger.info(f"  [OK] Products are correctly sorted by {filter_name}")
        take_screenshot(driver, self.screenshots_dir, "03_products_filtered")
        logger.info(
            f"\n[RESULT] Successfully filtered and verified {len(products)} products sorted by {filter_name}"
        )
