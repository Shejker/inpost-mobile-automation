def take_screenshot(driver, screenshots_dir, name):
    """Take and save screenshot with given name.

    Args:
        driver: Appium WebDriver instance.
        screenshots_dir: Directory path to save screenshot.
        name: Screenshot name without extension.

    Returns:
        Full filepath to saved screenshot.
    """
    filename = f"{name}.png"
    filepath = screenshots_dir / filename

    driver.save_screenshot(str(filepath))
    return str(filepath)
