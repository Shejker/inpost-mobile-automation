# Mobile Automation Project

Appium-based mobile automation framework for Android testing with Python and pytest.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Java JDK 17+
- Android SDK
- Appium Server with uiautomator2 driver (Android)
- Xcode + XCUITest driver (iOS, macOS only)
- Allure Report

**Developed on:** Windows 11 with Sony Xperia 5 IV XQ-CQ54 (Android 14, USB)

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2
appium driver install xcuitest  # For iOS testing
scoop install allure  # or download from https://github.com/allure-framework/allure2/releases

# 2. Configure environment
cp env.template .env
# Edit .env with your device UDID and app path

# 3. Connect device
adb devices
```

## Running Tests

### Local

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

### Docker Compose

```bash
# Set environment variables
export UDID=your_device_udid
export PLATFORM_VERSION=14
export APP_PATH=builds/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk
export APP_PACKAGE=com.swaglabsmobileapp
export APP_ACTIVITY=com.swaglabsmobileapp.MainActivity
export FULL_RESET=false

# Run tests in containers
docker-compose up --build

# Or just lint
docker-compose run tests ruff check .
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

## Multi-Platform Support

Examples for iOS and emulators are in:
- `config/capabilities.py` - Device configurations
- `tests/conftest_examples.py` - Alternative fixtures
- `tests/test_ios_example.py` - iOS test example

To use iOS/emulator: Copy fixture from `conftest_examples.py` to `conftest.py`
