"""Pytest configuration and fixtures for Playwright."""
import pytest
from playwright.sync_api import sync_playwright


def pytest_addoption(parser):
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="run tests in headed mode",
    )


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        headless = not pytest.config.getoption("--headed")
        browser = p.chromium.launch(headless=headless, slow_mo=500)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page = context.new_page()
    yield page
    context.close()