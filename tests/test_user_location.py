import pytest
from _pytest.fixtures import FixtureRequest
from selenium.webdriver.remote.webdriver import WebDriver

from tests.selectors import find_user_location


@pytest.mark.parametrize(
	"driver_fixture, expected_value",
	[
		("driver_with_location_permission", "!= 0"),
		("driver_without_location_permission", "== 0"),
	]
)
def test_user_location(request: FixtureRequest, driver_fixture: str, expected_value: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	th_elements = find_user_location(driver, timeout_value)

	assert th_elements, "No <th> elements found in <tbody>"
	assert len(th_elements) == 2, f"Expected 2 <th> elements, found {len(th_elements)}"

	for th_element in th_elements:
		assert th_element.is_displayed(), f"Element <th> is not visible: {th_element.text}"

		if expected_value == '!= 0':
			assert th_element.text != '0', f"Unexpected value in <th>: {th_element.text}"
		elif expected_value == '== 0':
			assert th_element.text == '0', f"Unexpected value in <th>: {th_element.text}"

		assert isinstance(float(th_element.text), float), f"<th> value is not a float: {th_element.text}"

	latitude, longitude = [float(th.text) for th in th_elements]
	assert -90 <= latitude <= 90, f"Latitude out of bounds: {latitude}"
	assert -180 <= longitude <= 180, f"Longitude out of bounds: {longitude}"
