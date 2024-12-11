import pytest
from _pytest.fixtures import FixtureRequest
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from tests.selectors import (
	find_selected_location,
	find_update_button,
	find_week_forecast_table_body_tr,
	find_week_forecast_table_header_th,
)
from tests.utils import create_random_valid_float, get_dynamic_days_order


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_week_forecast_table(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_head_th_elements = find_week_forecast_table_header_th(driver, timeout_value)
	assert len(table_head_th_elements) == 7, f"Expected 7 table headers, but found {len(table_head_th_elements)}"

	days = get_dynamic_days_order()
	days_from_table = [th.text for th in table_head_th_elements]
	assert days_from_table == days, f"Expected days: {days}, but got: {days_from_table}"

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)
	assert len(table_tbody_tr_elements) == 5, f"Expected 5 rows in tbody, but found {len(table_tbody_tr_elements)}"

	expected_row_names = ('Date', 'Weather', 'Max [°C]', 'Min [°C]', 'Generated\nenergy [kWh]')

	for idx, (row, expected_row_name) in enumerate(zip(table_tbody_tr_elements, expected_row_names)):
		actual_row_name = row.find_element(By.TAG_NAME, 'th').text
		assert actual_row_name == expected_row_name, (
			f"Row {idx + 1} header mismatch: expected '{expected_row_name}', but got '{actual_row_name}'"
		)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_week_forecast_table_changed_after_user_input(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	assert update_location_button.is_enabled()

	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)
	table_head_th_elements_before = [th.text for th in find_week_forecast_table_header_th(driver, timeout_value)]
	table_body_before = [
		[cell.text for cell in row.find_elements(By.TAG_NAME, 'th')]
		for row in find_week_forecast_table_body_tr(driver, timeout_value)
	]
	start_latitude_value = selected_latitude_input.get_attribute("value")
	start_longitude_value = selected_longitude_input.get_attribute("value")

	selected_latitude_input.clear()
	random_latitude_value = str(create_random_valid_float(latitude=True))
	selected_latitude_input.send_keys(random_latitude_value)

	selected_longitude_input.clear()
	random_longitude_value = str(create_random_valid_float(longitude=True))
	selected_longitude_input.send_keys(random_longitude_value)

	assert start_latitude_value != random_latitude_value or start_longitude_value != random_longitude_value

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(
		lambda d: [th.text for th in find_week_forecast_table_body_tr(d, timeout_value)] != table_body_before
	)

	table_head_th_elements_after = [th.text for th in find_week_forecast_table_header_th(driver, timeout_value)]
	table_body_after = [
		[cell.text for cell in row.find_elements(By.TAG_NAME, 'th')]
		for row in find_week_forecast_table_body_tr(driver, timeout_value)
	]

	assert table_head_th_elements_before == table_head_th_elements_after, (
		"Table headers change after updating the location"
	)
	assert table_body_before != table_body_after, "Table body did not change after updating the location"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_week_forecast_table_not_changed_after_same_user_input(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	assert update_location_button.is_enabled()

	table_head_th_elements_before = [th.text for th in find_week_forecast_table_header_th(driver, timeout_value)]
	table_body_before = [
		[cell.text for cell in row.find_elements(By.TAG_NAME, 'th')]
		for row in find_week_forecast_table_body_tr(driver, timeout_value)
	]

	update_location_button.click()

	table_head_th_elements_after = [th.text for th in find_week_forecast_table_header_th(driver, timeout_value)]
	table_body_after = [
		[cell.text for cell in row.find_elements(By.TAG_NAME, 'th')]
		for row in find_week_forecast_table_body_tr(driver, timeout_value)
	]

	assert table_head_th_elements_before == table_head_th_elements_after, (
		"Table headers changed after updating the location"
	)
	assert table_body_before == table_body_after, "Table body changed after updating the location"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_date_row_in_week_forecast_table(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)

	date_row_element = table_tbody_tr_elements[0]
	th_date_row_elements = date_row_element.find_elements(By.TAG_NAME, 'th')[1:]
	assert len(th_date_row_elements) == 7, f"Expected 7 columns, but found {len(th_date_row_elements)}"

	for idx, th_element in enumerate(th_date_row_elements):
		assert th_element.is_displayed(), f"Column {idx + 1} is not visible"
		assert th_element.text, f"Column {idx + 1}  has no text"

		assert '/' in th_element.text, f"Text '{th_element.text}' does not contain '/'"

		date_parts = th_element.text.split('/')
		assert len(date_parts) == 3, f"Date '{th_element.text}' does not have 3 parts"

		day, month, year = map(int, date_parts)
		assert 1 <= day <= 31, f"Day '{day}' is out of range"
		assert 1 <= month <= 12, f"Month '{month}' is out of range"
		assert year > 2000, f"Year '{year}' is out of range"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_weather_row_in_week_forecast_table(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)

	date_row_element = table_tbody_tr_elements[1]
	th_date_row_elements = date_row_element.find_elements(By.TAG_NAME, 'th')[1:]
	assert len(th_date_row_elements) == 7, f"Expected 7 columns, but found {len(th_date_row_elements)}"

	for idx, th_element in enumerate(th_date_row_elements):
		assert th_element.is_displayed(), f"Column {idx + 1} is not visible"

		try:
			svg_element = th_element.find_element(By.TAG_NAME, 'svg')
			assert svg_element.is_displayed()
		except NoSuchElementException:
			raise AssertionError(f"No SVG icon found in column {idx + 1}")


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_max_temp_row_in_week_forecast_table(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)

	date_row_element = table_tbody_tr_elements[2]
	th_date_row_elements = date_row_element.find_elements(By.TAG_NAME, 'th')[1:]
	assert len(th_date_row_elements) == 7, f"Expected 7 columns, but found {len(th_date_row_elements)}"

	for idx, th_element in enumerate(th_date_row_elements):
		assert th_element.is_displayed(), f"Column {idx + 1} is not visible"
		assert th_element.text, f"Column {idx + 1}  has no text"

		try:
			temperature = float(th_element.text)
			assert isinstance(temperature, float), (
				f"Column {idx + 1} does not contain a valid float: '{th_element.text}'"
			)
			assert -95 <= temperature <= 60, f"Temperature in column {idx + 1} is out of range: {temperature}"

		except ValueError:
			raise AssertionError(f"Column {idx + 1} contains non-numeric value: '{th_element.text}'")


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_min_temp_row_in_week_forecast_table(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)

	date_row_element = table_tbody_tr_elements[3]
	th_date_row_elements = date_row_element.find_elements(By.TAG_NAME, 'th')[1:]
	assert len(th_date_row_elements) == 7, f"Expected 7 columns, but found {len(th_date_row_elements)}"

	for idx, th_element in enumerate(th_date_row_elements):
		assert th_element.is_displayed(), f"Column {idx + 1} is not visible"
		assert th_element.text, f"Column {idx + 1}  has no text"

		try:
			temperature = float(th_element.text)
			assert isinstance(temperature, float), (
				f"Column {idx + 1} does not contain a valid float: '{th_element.text}'"
			)
			assert -95 <= temperature <= 60, f"Temperature in column {idx + 1} is out of range: {temperature}"

		except ValueError:
			raise AssertionError(f"Column {idx + 1} contains non-numeric value: '{th_element.text}'")


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_generated_energy_row_in_week_forecast_table(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	table_tbody_tr_elements = find_week_forecast_table_body_tr(driver, timeout_value)

	date_row_element = table_tbody_tr_elements[-1]
	th_date_row_elements = date_row_element.find_elements(By.TAG_NAME, 'th')[1:]
	assert len(th_date_row_elements) == 7, f"Expected 7 columns, but found {len(th_date_row_elements)}"

	for idx, th_element in enumerate(th_date_row_elements):
		assert th_element.is_displayed(), f"Column {idx + 1} is not visible"
		assert th_element.text, f"Column {idx + 1}  has no text"

		try:
			energy_value = float(th_element.text)
			assert isinstance(energy_value, float), (
				f"Column {idx + 1} does not contain a valid float: '{th_element.text}'"
			)
			assert energy_value >= 0, f"Energy in column {idx + 1} is negative: {energy_value}"

		except ValueError:
			raise AssertionError(f"Column {idx + 1} contains non-numeric value: '{th_element.text}'")
