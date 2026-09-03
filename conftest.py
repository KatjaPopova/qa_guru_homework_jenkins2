import os
from urllib.parse import quote

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import attach

load_dotenv()


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default=(
            "https://demoqa.com/automation-practice-form"
        ),
        help="Адрес тестируемой страницы",
    )

    parser.addoption(
        "--remote-url",
        action="store",
        default="https://selenoid.qa.guru/wd/hub",
        help="Адрес Selenoid",
    )

    parser.addoption(
        "--browser",
        action="store",
        choices=["chrome", "firefox"],
        default="chrome",
        help="Браузер: chrome или firefox",
    )

    parser.addoption(
        "--browser-version",
        action="store",
        default="148.0",
        help="Версия браузера",
    )

    parser.addoption(
        "--headless",
        action="store",
        choices=["true", "false"],
        default="false",
        help="Headless-режим: true или false",
    )

    parser.addoption(
        "--window-size",
        action="store",
        default="1920x1080",
        help="Разрешение экрана, например 1920x1080",
    )


def get_window_size(value):
    try:
        width, height = value.lower().split("x")
        return int(width), int(height)
    except ValueError:
        raise pytest.UsageError(
            "--window-size нужно указать в формате 1920x1080"
        )


@pytest.fixture(scope="function")
def driver(request):
    login = os.getenv("LOGIN")
    password = os.getenv("PASSWORD")

    if not login:
        pytest.fail("В файле .env не указана переменная LOGIN")

    if not password:
        pytest.fail("В файле .env не указана переменная PASSWORD")

    base_url = request.config.getoption("--base-url")
    remote_url = request.config.getoption("--remote-url")
    browser_name = request.config.getoption("--browser")
    browser_version = request.config.getoption("--browser-version")
    headless = request.config.getoption("--headless") == "true"
    window_size = request.config.getoption("--window-size")

    width, height = get_window_size(window_size)

    if browser_name == "chrome":
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={width},{height}")

    elif browser_name == "firefox":
        options = FirefoxOptions()

        if headless:
            options.add_argument("-headless")

        options.add_argument(f"--width={width}")
        options.add_argument(f"--height={height}")

    else:
        raise pytest.UsageError(
            f"Неизвестный браузер: {browser_name}"
        )

    options.browser_version = browser_version

    options.set_capability(
        "selenoid:options",
        {
            "enableVNC": True,
            "enableVideo": True,
            "screenResolution": f"{width}x{height}x24",
        },
    )

    encoded_login = quote(login, safe="")
    encoded_password = quote(password, safe="")

    if "://" not in remote_url:
        raise pytest.UsageError(
            "--remote-url должен начинаться с http:// или https://"
        )

    command_executor = remote_url.replace(
        "://",
        f"://{encoded_login}:{encoded_password}@",
        1,
    )

    driver = webdriver.Remote(
        command_executor=command_executor,
        options=options,
    )

    driver.set_window_size(width, height)
    driver.base_url = base_url

    yield driver

    try:
        attach.add_screenshot(driver)
        attach.add_html(driver)
        attach.add_logs(driver)
        attach.add_video(driver)
    finally:
        driver.quit()
