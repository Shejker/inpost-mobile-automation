# Mobile Automation Project

Appium-based mobile automation framework for Android testing with Python and pytest.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Java JDK 17+
- Android SDK
- Appium Server with uiautomator2 driver
- Allure Report

**Developed on:** Windows 11 with physical Android device (USB)

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2
scoop install allure  # or download from https://github.com/allure-framework/allure2/releases

# 2. Configure environment
cp env.template .env
# Edit .env with your device UDID and app path

# 3. Connect device
adb devices
```

## Running Tests

```bash
# Start Appium server
appium

# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_filter_products.py -v -s

# Run with markers
pytest -m smoke -v
```

## Generate Reports

```bash
# Run tests and generate Allure report
pytest tests/ -v --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report
```

## Code Quality

```bash
# Check code
ruff check .

# Fix issues
ruff check . --fix

# Format code
ruff format .
```

## Project Structure

```
├── config/              # Configuration
├── pages/               # Page Object Model
├── tests/               # Test cases
├── utils/               # Helpers
├── builds/              # APK files
└── results/             # Test results & logs
```

## Tests

- `test_cart_remove.py` - Remove items from cart
- `test_filter_products.py` - Filter & sort products
- `test_form_validation.py` - Form validation
- `test_e2e_complete_purchase.py` - Complete purchase flow
