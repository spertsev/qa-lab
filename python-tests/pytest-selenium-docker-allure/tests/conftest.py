import os
import sys
import pytest
from selenium import webdriver

from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.webdriver import WebDriver as SafariDriver


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser: chrome | chromium | firefox | edge | safari",
    )
    parser.addoption(
        "--headless",
        action="store",
        default="off",
        help="Headless mode: on | off (default: off)",
    )


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    headless_mode = request.config.getoption("--headless").lower()
    remote_url = os.environ.get("SELENIUM_REMOTE_URL")

    # --- Chrome ---
    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        if headless_mode == "on":
            # Современный headless-режим и флаги для работы в контейнере
            options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")

        if remote_url:
            # Работа через Selenium Grid / standalone-chrome
            driver = webdriver.Remote(command_executor=remote_url, options=options)
        else:
            # Локальный запуск
            driver = webdriver.Chrome(options=options)

    # --- Firefox ---
    elif browser_name == "firefox":
        options = FirefoxOptions()
        options.set_preference("browser.startup.homepage", "about:blank")
        if headless_mode == "on":
            options.add_argument("--headless")

        if remote_url:
            # В docker-compose используется selenium/standalone-chrome,
            # поэтому remote-режим поддерживаем только для Chrome.
            raise RuntimeError(
                "Remote Selenium в docker поддерживается только для Chrome"
            )
        driver = webdriver.Firefox(options=options)

    # --- Edge ---
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless_mode == "on":
            options.add_argument("--headless")

        if remote_url:
            raise RuntimeError(
                "Remote Selenium в docker поддерживается только для Chrome"
            )
        driver = webdriver.Edge(options=options)

    # --- Safari (macOS only) ---
    elif browser_name == "safari":
        if sys.platform != "darwin":
            raise RuntimeError("Safari поддерживается только на macOS")
        if headless_mode == "on":
            raise RuntimeError("Safari не поддерживает headless режим")
        if remote_url:
            raise RuntimeError(
                "Remote Selenium в docker поддерживается только для Chrome"
            )
        driver = SafariDriver()

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.implicitly_wait(5)

    yield driver
    driver.quit()
