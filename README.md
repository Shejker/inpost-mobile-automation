# Mobile Automation Project

Appium-based mobile automation framework for Android and iOS testing.

## Prerequisites

- Python 3.12+
- Node.js 20+
- Java JDK 17+
- Android SDK
- Appium Server

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Appium:
```bash
npm install -g appium
appium driver install uiautomator2
```

3. Create `.env` file from template:
```bash
cp env.template .env
```

4. Update `.env` with your device settings.

## Running Tests

Start Appium server:
```bash
appium
```

Run all tests:
```bash
pytest
```

Run specific test:
```bash
pytest tests/test_shopping_cart.py
```

Run with markers:
```bash
pytest -m smoke
```

## Project Structure

```
├── config/          # Configuration files
├── pages/           # Page Object Model classes
├── tests/           # Test cases
├── utils/           # Helper functions
└── requirements.txt # Python dependencies
```