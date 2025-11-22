from pathlib import Path
from datetime import datetime


def take_screenshot(driver, test_name):
    screenshots_dir = Path(__file__).resolve().parent.parent / 'screenshots'
    screenshots_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{test_name}_{timestamp}.png"
    filepath = screenshots_dir / filename
    
    driver.save_screenshot(str(filepath))
    return str(filepath)