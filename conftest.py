import pytest
from selenium import webdriver


@pytest.fixture()
def driver():
    chrome_options = webdriver.ChromeOptions()

    HEADLESS_MODE = True

    if HEADLESS_MODE:
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    if not HEADLESS_MODE:
        driver.maximize_window()

    driver.implicitly_wait(5)
    yield driver
    driver.quit()