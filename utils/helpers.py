def take_screenshot(driver, screenshots_dir, name):
    filename = f"{name}.png"
    filepath = screenshots_dir / filename

    driver.save_screenshot(str(filepath))
    return str(filepath)
