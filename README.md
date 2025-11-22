# Mobile Automation Project

Appium-based mobile automation framework for Android testing with Python and pytest.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Java JDK 17+
- Android SDK with platform-tools
- Appium Server with uiautomator2 driver

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Appium

```bash
npm install -g appium
appium driver install uiautomator2
```

### 3. Configure environment

Create `.env` file from template:

```bash
cp env.template .env
```

### 4. Update .env for Sauce Labs Demo App

For the Sauce Labs mobile sample application, add:

```
APPIUM_SERVER=http://localhost:4723
UDID=<your_device_udid>
APP_PATH=builds/Android.SauceLabs.Mobile.Sample.app.2.7.1.apk
APP_PACKAGE=com.swaglabsmobileapp
APP_ACTIVITY=com.swaglabsmobileapp.MainActivity
FULL_RESET=false
```

Where:
- `UDID` - Get from `adb devices`
- `APP_PATH` - Path to APK file (relative to project root)
- `APP_PACKAGE` - Application package name
- `APP_ACTIVITY` - Main activity to launch
- `FULL_RESET` - Set to `true` for first run, `false` for faster subsequent runs

### 5. Connect Android device

Enable USB Debugging on your device and connect via USB.

Verify connection:

```bash
adb devices
```

## Running Tests

Start Appium server:

```bash
appium
```

Run tests:

```bash
pytest tests/ -v
```

Run specific test:

```bash
pytest tests/test_e2e_complete_flow.py -v -s
```

Run with markers:

```bash
pytest -m smoke -v
```

## Project Structure

```
├── config/              # Configuration and settings
├── pages/               # Page Object Model classes
├── tests/               # Test cases
├── utils/               # Helper functions
├── builds/              # APK files
├── results/             # Test results
│   ├── logs/            # Test logs (appium.log)
│   └── {timestamp}/     # Test run results with screenshots
└── README.md
```

## Test Results

After running tests, results are organized in `results/` directory:
- `results/logs/appium.log` - Appium server logs
- `results/{timestamp}/screenshots/` - Screenshots from test run (01_*, 02_*, etc.)
