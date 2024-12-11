import random

import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from tests.selectors import find_error_messages, find_selected_location, find_update_button, find_user_location
from tests.utils import create_random_invalid_float, create_random_non_float


@pytest.mark.parametrize(
	"driver_fixture, expected_input_value",
	[
		("driver_with_location_permission", "!= 0"),
		("driver_without_location_permission", "== 0")
	]
)
def test_default_selected_location(
		request: FixtureRequest, driver_fixture: str, expected_input_value: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	input_elements = find_selected_location(driver, timeout_value)

	assert input_elements, "No <input> elements found in <div>"
	assert len(input_elements) == 2, f'Expected 2 <input> elements, found {len(input_elements)}'

	for input_element in input_elements:
		input_value = input_element.get_attribute("value")

		assert input_element.is_displayed(), f"Element <input> is not visible: {input_value}"

		if expected_input_value == '!= 0':
			assert input_value != '0', f"Unexpected value in <input>: {input_value}"
		elif expected_input_value == '== 0':
			assert input_value == '0', f"Unexpected value in <input>: {input_value}"

		assert isinstance(float(input_value), float), f"<input> value is not a float: {input_value}"

	selected_latitude, selected_longitude = [
		float(input_element.get_attribute("value")) for input_element in input_elements
	]
	user_latitude, user_longitude = [float(th.text) for th in find_user_location(driver, timeout_value)]

	assert user_latitude == selected_latitude, f"Latitude mismatch: {user_latitude} != {selected_latitude}"
	assert user_longitude == selected_longitude, f"Longitude mismatch: {user_longitude} != {selected_longitude}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_change_latitude_in_selected_location(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(
		driver, timeout_value
	)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	start_latitude_value = selected_latitude_input.get_attribute("value")
	start_longitude_value = selected_longitude_input.get_attribute("value")

	random_latitude_value = str(round(random.uniform(-90, 90), 4))

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(
		lambda d: selected_latitude_input.get_attribute("value") == random_latitude_value
	)

	actual_latitude_value = selected_latitude_input.get_attribute("value")
	actual_longitude_value = selected_longitude_input.get_attribute("value")

	assert actual_latitude_value != start_latitude_value, (
		f"Latitude did not change. Start: {start_latitude_value}, Actual: {actual_latitude_value}"
	)
	assert actual_latitude_value == random_latitude_value, (
		f"Expected latitude to be {random_latitude_value}, but got {actual_latitude_value}"
	)

	assert actual_longitude_value == start_longitude_value, (
		f"Expected longitude to remain {start_longitude_value}, but got {actual_longitude_value}"
	)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_change_longitude_in_selected_location(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	start_latitude_value = selected_latitude_input.get_attribute("value")
	start_longitude_value = selected_longitude_input.get_attribute("value")

	random_longitude_value = str(round(random.uniform(-180, 180), 4))

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(
		lambda d: selected_longitude_input.get_attribute("value") == random_longitude_value
	)

	actual_latitude_value = selected_latitude_input.get_attribute("value")
	actual_longitude_value = selected_longitude_input.get_attribute("value")

	assert actual_longitude_value != start_longitude_value, (
		f"Longitude did not change. Start: {start_longitude_value}, Actual: {actual_longitude_value}"
	)
	assert actual_longitude_value == random_longitude_value, (
		f"Expected longitude to be {random_longitude_value}, but got {actual_longitude_value}"
	)

	assert actual_latitude_value == start_latitude_value, (
		f"Expected latitude to remain {start_latitude_value}, but got {actual_latitude_value}"
	)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_change_whole_selected_location(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	start_latitude_value = selected_latitude_input.get_attribute("value")
	start_longitude_value = selected_longitude_input.get_attribute("value")

	random_latitude_value = str(round(random.uniform(-90, 90), 4))
	random_longitude_value = str(round(random.uniform(-180, 180), 4))

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(
		lambda d: selected_latitude_input.get_attribute("value") == random_latitude_value
	)
	WebDriverWait(driver, timeout_value).until(
		lambda d: selected_longitude_input.get_attribute("value") == random_longitude_value
	)

	actual_latitude_value = selected_latitude_input.get_attribute("value")
	actual_longitude_value = selected_longitude_input.get_attribute("value")

	assert actual_latitude_value != start_latitude_value, (
		f"Latitude did not change. Start: {start_latitude_value}, Actual: {actual_latitude_value}"
	)
	assert actual_latitude_value == random_latitude_value, (
		f"Expected latitude to be {random_latitude_value}, but got {actual_latitude_value}"
	)
	assert actual_longitude_value != start_longitude_value, (
		f"Longitude did not change. Start: {start_longitude_value}, Actual: {actual_longitude_value}"
	)
	assert actual_longitude_value == random_longitude_value, (
		f"Expected longitude to be {random_longitude_value}, but got {actual_longitude_value}"
	)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_change_nothing_in_selected_location(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	start_latitude_value = selected_latitude_input.get_attribute("value")
	start_longitude_value = selected_longitude_input.get_attribute("value")

	update_location_button.click()

	actual_latitude_value = selected_latitude_input.get_attribute("value")
	actual_longitude_value = selected_longitude_input.get_attribute("value")

	assert actual_latitude_value == start_latitude_value, (
		f"Latitude changed. Start: {start_latitude_value}, Actual: {actual_latitude_value}"
	)

	assert actual_longitude_value == start_longitude_value, (
		f"Longitude changed. Start: {start_longitude_value}, Actual: {actual_longitude_value}"
	)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_float_latitude_input(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_latitude_value = create_random_invalid_float(latitude=True)

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_float_longitude_input(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_longitude_value = create_random_invalid_float(longitude=True)

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_float_inputs(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_latitude_value = create_random_invalid_float(latitude=True)
	random_longitude_value = create_random_invalid_float(longitude=True)

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_no_float_latitude_input(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_latitude_value = create_random_non_float(10)

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_no_float_longitude_input(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_longitude_value = create_random_non_float(10)

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_invalid_no_float_inputs(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)

	assert update_location_button.is_displayed(), "Update button is not visible"
	assert selected_latitude_input.is_displayed(), "Latitude input is not visible"
	assert selected_longitude_input.is_displayed(), "Longitude input is not visible"

	random_latitude_value = create_random_non_float(10)
	random_longitude_value = create_random_non_float(10)

	selected_latitude_input.clear()
	selected_latitude_input.send_keys(random_latitude_value)

	selected_longitude_input.clear()
	selected_longitude_input.send_keys(random_longitude_value)

	update_location_button.click()

	WebDriverWait(driver, timeout_value).until(lambda d: len(find_error_messages(d, timeout_value)) > 0)

	div_error_messages = find_error_messages(driver, timeout_value)
	assert len(div_error_messages) > 0, "No error messages found"

	for idx, error_msg in enumerate(div_error_messages):
		assert error_msg.is_displayed(), f"Error message {idx + 1} is not visible"
		assert 'Something went wrong' in error_msg.text, f"Unexpected error message: {error_msg.text}"
