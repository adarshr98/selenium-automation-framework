import base64
import html
import os
from datetime import datetime
import pytest
from selenium import webdriver

import pytest_html
from pytest_html import extras  # ✅ Make sure this is imported


from pytest_html import extras

def pytest_addoption(parser):
    parser.addoption(
        "--browser_name", action="store", default="chrome", help="browser selection"
    )

@pytest.fixture(scope="function")
def browserInstance(request):
    global driver
    browser_name = request.config.getoption("--browser_name")
    if browser_name == "chrome":
        driver = webdriver.Chrome()
    if browser_name == "firefox":
        driver = webdriver.Firefox()

    driver.get("https://www.saucedemo.com/")
    driver.maximize_window()
    driver.implicitly_wait(5)

    yield driver
    driver.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == 'call' and rep.failed:
        driver = item.funcargs.get("browserInstance")
        if driver is not None:
            screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            file_name = f"{item.name}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.png"
            file_path = os.path.join(screenshot_dir, file_name)
            driver.save_screenshot(file_path)

            # Attach to report manually using HTML
            extra = getattr(rep, 'extra', [])
            if os.path.exists(file_path):
                html_content = f'<div><a href="screenshots/{file_name}" target="_blank"><img src="screenshots/{file_name}" alt="screenshot" width="300"/></a></div>'
                extra.append(pytest_html.extras.html(html_content))
            rep.extra = extra

# -------------------- Add 'Screenshot' column --------------------
def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Screenshot</th>")

def pytest_html_results_table_row(report, cells):
    screenshot_html = ''
    for extra in getattr(report, 'extra', []):
        if extra.get('format') == 'html':
            screenshot_html = extra['content']
    cells.insert(2, f"<td>{screenshot_html}</td>")