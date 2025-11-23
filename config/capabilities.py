from appium.options.android import UiAutomator2Options
from appium.options.ios import XCUITestOptions


def get_android_capabilities(platform_version=None, udid=None, app_path=None):
    """Android physical device capabilities"""
    options = UiAutomator2Options()
    if platform_version:
        options.platform_version = platform_version
    if udid:
        options.udid = udid
    if app_path:
        options.app = app_path
    options.app_wait_duration = 30000
    return options


def get_android_emulator_capabilities(app_path=None):
    """Android emulator capabilities"""
    options = UiAutomator2Options()
    options.device_name = "emulator-5554"
    options.platform_version = "14"
    if app_path:
        options.app = app_path
    options.app_wait_duration = 30000
    options.no_reset = True
    return options


def get_ios_capabilities(platform_version=None, udid=None, app_path=None):
    """iOS physical device capabilities"""
    options = XCUITestOptions()
    if platform_version:
        options.platform_version = platform_version
    if udid:
        options.udid = udid
    if app_path:
        options.app = app_path
    options.automation_name = "XCUITest"
    options.app_wait_duration = 30000
    return options


def get_ios_simulator_capabilities(app_path=None):
    """iOS simulator capabilities"""
    options = XCUITestOptions()
    options.device_name = "iPhone 15"
    options.platform_version = "17.0"
    if app_path:
        options.app = app_path
    options.automation_name = "XCUITest"
    options.app_wait_duration = 30000
    options.no_reset = True
    return options
