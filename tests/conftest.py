import os

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.remote.webdriver import WebDriver

load_dotenv()
url = os.getenv("URL")


@pytest.fixture()
def driver() -> WebDriver:
	driver = webdriver.Chrome()
	driver.get(url)
	yield driver
	driver.quit()


@pytest.fixture()
def driver_with_location_permission() -> WebDriver:
	options = ChromeOptions()
	prefs = {
		'profile.default_content_setting_values.geolocation': 1
	}

	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	yield driver
	driver.quit()


@pytest.fixture()
def driver_without_location_permission() -> WebDriver:
	options = ChromeOptions()
	prefs = {
		'profile.default_content_setting_values.geolocation': 2
	}

	options.add_experimental_option('prefs', prefs)
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	yield driver
	driver.quit()


@pytest.fixture()
def timeout_value() -> int:
	return 15
