import pytest
from _pytest.fixtures import FixtureRequest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from .selectors import find_selected_location, find_update_button, find_week_summary_div
from .utils import create_random_valid_float


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_week_summary(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	div_summary_element = find_week_summary_div(driver, timeout_value)

	inner_divs = div_summary_element.find_elements(By.XPATH, ".//div[contains(@class, 'col-12 col-md-6 col-lg-3')]")
	assert len(inner_divs) == 4, f"Expected 4 inner divs, but found {len(inner_divs)}"

	for idx, inner_div in enumerate(inner_divs):
		assert inner_div.is_displayed(), f"Inner div {idx + 1} is not visible"
		assert inner_div.text.strip(), f"Inner div {idx + 1} has no text"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_week_summary_changed_after_user_input(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver: WebDriver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	assert update_location_button.is_enabled(), "Update location button is not enabled"

	selected_latitude_input, selected_longitude_input = find_selected_location(driver, timeout_value)
	initial_summary_text = find_week_summary_div(driver, timeout_value).text

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
		lambda d: find_week_summary_div(d, timeout_value).text != initial_summary_text
	)

	updated_summary_text = find_week_summary_div(driver, timeout_value).text

	assert initial_summary_text != updated_summary_text, (
		"Week summary text did not change after updating the location"
	)


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_week_summary_not_changed_after_same_user_input(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver = request.getfixturevalue(driver_fixture)

	update_location_button = find_update_button(driver, timeout_value)
	assert update_location_button.is_enabled(), "Update location button is not enabled"

	initial_summary_text = find_week_summary_div(driver, timeout_value).text

	update_location_button.click()

	updated_summary_text = find_week_summary_div(driver, timeout_value).text

	assert initial_summary_text == updated_summary_text, "Week summary text changed after updating the location"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_temperatures_in_week_summary(request: FixtureRequest, driver_fixture: str, timeout_value: int) -> None:
	driver = request.getfixturevalue(driver_fixture)

	div_summary_element = find_week_summary_div(driver, timeout_value)
	temperatures_div = div_summary_element.find_elements(
		By.XPATH,
		".//div[contains(@class, 'col-12 col-md-6 col-lg-3')]"
	)[0]
	inner_temperature_spans = temperatures_div.find_elements(By.TAG_NAME, "span")

	assert len(inner_temperature_spans) == 2

	for idx, inner_span in enumerate(inner_temperature_spans):
		assert inner_span.is_displayed(), f"Expected 2 spans, but found {len(inner_temperature_spans)}"

		try:
			svg_element = inner_span.find_element(By.TAG_NAME, 'svg')
			assert svg_element.is_displayed(), f"SVG in span {idx + 1} is not visible"

		except NoSuchElementException:
			raise AssertionError(f"No SVG icon found in span {idx + 1}")

	max_temp_element, min_temp_element = [inner_span for inner_span in inner_temperature_spans]
	max_svg_icon = max_temp_element.find_element(By.TAG_NAME, 'svg').get_attribute("data-icon")
	min_svg_icon = min_temp_element.find_element(By.TAG_NAME, 'svg').get_attribute("data-icon")

	assert max_svg_icon == "temperature-full", f"Unexpected icon in max temperature: {max_svg_icon}"
	assert min_svg_icon == "temperature-empty", f"Unexpected icon in min temperature: {min_svg_icon}"

	max_temp = max_temp_element.text.split(' ')

	assert max_temp[0] == 'Max:', f"Expected 'Max:' but found {max_temp[0]}"
	assert isinstance(float(max_temp[1]), float), f"Max temperature value is not a float: {max_temp[1]}"
	assert max_temp[-1] == "[°C]", f"Expected '[°C]' but found {max_temp[-1]}"

	min_temp = min_temp_element.text.split(' ')

	assert min_temp[0] == 'Min:', f"Expected 'Min:' but found {min_temp[0]}"
	assert isinstance(float(min_temp[1]), float), f"Min temperature value is not a float: {min_temp[1]}"
	assert min_temp[-1] == "[°C]", f"Expected '[°C]' but found {min_temp[-1]}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_average_pressure_in_week_summary(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver = request.getfixturevalue(driver_fixture)

	div_summary_element = find_week_summary_div(driver, timeout_value)
	pressure_div = div_summary_element.find_elements(
		By.XPATH,
		".//div[contains(@class, 'col-12 col-md-6 col-lg-3')]"
	)[1]
	inner_pressure_span = pressure_div.find_element(By.TAG_NAME, "span")
	assert inner_pressure_span.is_displayed(), "Pressure span is not visible"

	pressure_svg_icon = inner_pressure_span.find_element(By.TAG_NAME, 'svg')
	assert pressure_svg_icon.is_displayed(), "Pressure SVG icon is not visible"
	assert pressure_svg_icon.get_attribute("data-icon") == "arrows-down-to-line", (
		f"Unexpected icon in pressure span: {pressure_svg_icon.get_attribute('data-icon')}"
	)

	pressure_text = inner_pressure_span.text.split(' ')
	assert len(pressure_text) == 2, f"Pressure text is not in expected format: {pressure_text}"

	assert isinstance(float(pressure_text[0]), float), f"Pressure value is not a float: {pressure_text[0]}"
	assert pressure_text[-1] == "[hPa]", f"Expected '[hPa]' but found {pressure_text[-1]}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_average_sunshine_duration_in_week_summary(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver = request.getfixturevalue(driver_fixture)

	div_summary_element = find_week_summary_div(driver, timeout_value)
	sunshine_duration_div = div_summary_element.find_elements(
		By.XPATH,
		".//div[contains(@class, 'col-12 col-md-6 col-lg-3')]"
	)[2]
	inner_sunshine_span = sunshine_duration_div.find_element(By.TAG_NAME, "span")
	assert inner_sunshine_span.is_displayed(), "Sunshine duration span is not visible"

	sunshine_duration_svg_icon = inner_sunshine_span.find_element(By.TAG_NAME, 'svg')
	assert sunshine_duration_svg_icon.is_displayed(), "Sunshine duration SVG icon is not visible"
	assert sunshine_duration_svg_icon.get_attribute("data-icon") == "solar-panel", (
		f"Unexpected icon in sunshine duration span: {sunshine_duration_svg_icon.get_attribute('data-icon')}"
	)

	sunshine_duration_text = inner_sunshine_span.text.split(' ')
	assert len(sunshine_duration_text) == 2, (
		f"Sunshine duration text is not in expected format: {sunshine_duration_text}"
	)

	hours_text = sunshine_duration_text[0]
	assert isinstance(int(hours_text[:-1]), int), f"Sunshine duration hours value is not int: {hours_text}"
	assert int(hours_text[:-1]) >= 0, f"Hours value should be non-negative, but found: {hours_text[:-1]}"
	assert hours_text[-1] == "h", f"Expected 'h' at the end of hours value, but found {hours_text[-1]}"

	minutes_text = sunshine_duration_text[1]
	assert isinstance(int(minutes_text[:-3]), int), f"Sunshine duration minutes value is not int: {minutes_text}"
	assert 0 <= int(minutes_text[:-3]) < 60, f"Minutes value should be between 0 and 59, but found: {minutes_text[:-3]}"
	assert minutes_text[-3:] == "min", f"Expected 'min' at the end of minutes value, but found {minutes_text[-3:]}"


@pytest.mark.parametrize(
	"driver_fixture",
	["driver_with_location_permission", "driver_without_location_permission"]
)
def test_display_weather_description_in_week_summary(
		request: FixtureRequest, driver_fixture: str, timeout_value: int
) -> None:
	driver = request.getfixturevalue(driver_fixture)

	div_summary_element = find_week_summary_div(driver, timeout_value)
	weather_description_div = div_summary_element.find_elements(
		By.XPATH,
		".//div[contains(@class, 'col-12 col-md-6 col-lg-3')]"
	)[-1]

	inner_weather_description_span = weather_description_div.find_element(By.TAG_NAME, "span")
	assert inner_weather_description_span.is_displayed(), "Weather description span is not visible"

	weather_description_svg_icon = inner_weather_description_span.find_element(By.TAG_NAME, 'svg')
	assert weather_description_svg_icon.is_displayed(), "Weather_description SVG icon is not visible"
	assert weather_description_svg_icon.get_attribute("data-icon") == "circle-info", (
		f"Unexpected icon in weather_description span: {weather_description_svg_icon.get_attribute('data-icon')}"
	)

	inner_weather_description_div = inner_weather_description_span.find_element(By.TAG_NAME, "div")
	paragraphs_elements = inner_weather_description_div.find_elements(By.TAG_NAME, "p")
	assert len(paragraphs_elements) >= 1, "Expected at least 1 paragraph in weather description, but found none"

	for idx, paragraph in enumerate(paragraphs_elements):
		assert paragraph.is_displayed(), f"Paragraph {idx + 1} in weather description is not visible"
		assert paragraph.text.strip(), f"Paragraph {idx + 1} in weather description is empty"
