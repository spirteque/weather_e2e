from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.utils import handle_exceptions

# TODO ids or data attributes for frontend rather than nested selectors


@handle_exceptions
def find_user_location(driver: WebDriver, timeout: int) -> list[WebElement]:
	div_element = WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//div[h3[contains(text(), 'Your location')]]"
			)
		)
	)
	tbody_element = div_element.find_element(By.TAG_NAME, 'tbody')

	return tbody_element.find_elements(By.TAG_NAME, 'th')


@handle_exceptions
def find_selected_location(driver: WebDriver, timeout: int) -> list[WebElement]:
	div_element = WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//div[h3[contains(text(), 'Selected location')]]"
			)
		)
	)

	return [
		div_element.find_element(By.XPATH, ".//input[@id='latitude-input']"),
		div_element.find_element(By.XPATH, ".//input[@id='longitude-input']")
	]


@handle_exceptions
def find_update_button(driver: WebDriver, timeout: int) -> WebElement:
	return WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//button[text()='Update location']"
			)
		)
	)


@handle_exceptions
def find_error_messages(driver: WebDriver, timeout: int) -> list[WebElement]:
	WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//div[contains(@class, 'alert-danger') and @role='alert']"
			)
		)
	)

	return driver.find_elements(By.XPATH, "//div[contains(@class, 'alert-danger') and @role='alert']")


@handle_exceptions
def find_week_forecast_table(driver: WebDriver, timeout: int) -> WebElement:
	div_element = WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//div[contains(@class, 'overflow-x-auto')]"
			)
		)
	)

	return div_element.find_element(By.TAG_NAME, 'table')


@handle_exceptions
def find_week_forecast_table_header_th(driver: WebDriver, timeout: int) -> list[WebElement]:
	table_element = find_week_forecast_table(driver, timeout)
	tr_element = table_element.find_element(By.TAG_NAME, 'tr')

	return tr_element.find_elements(By.CLASS_NAME, 'align-middle')


@handle_exceptions
def find_week_forecast_table_body_tr(driver: WebDriver, timeout: int) -> list[WebElement]:
	table_element = find_week_forecast_table(driver, timeout)
	tbody_element = table_element.find_element(By.TAG_NAME, 'tbody')

	return tbody_element.find_elements(By.TAG_NAME, 'tr')


@handle_exceptions
def find_week_summary_div(driver: WebDriver, timeout: int) -> WebElement:
	return WebDriverWait(driver, timeout).until(
		expected_conditions.presence_of_element_located(
			(
				By.XPATH,
				"//div[contains(@class, 'row mb-3') and .//div[contains(@class, 'col-12 col-md-6 col-lg-3')]]"
			)
		)
	)
