# Weather Application with Photovoltaic Energy Forecast: E2E Tests

This repository contains automated tests for the Weather Application frontend. The tests are written in Python using the `Selenium` framework and `pytest` for execution. These tests validate various UI elements and interactions on the frontend, ensuring the application's functionality meets expectations.

Frontend: [React Frontend Repository](https://github.com/spirteque/weather_frontend)

Backend: [FastAPI Backend Repository](https://github.com/spirteque/weather_backend)

Working website: [Weather Application](https://www.weather.spirteque.com)

External API: [Open-Meteo API](https://open-meteo.com/)

## Setup

To run the tests, you need the following:

### Prerequisites

1. Python 3.12
2. Google Chrome browser
3. Virtual environment (recommended)
4. Dependencies listed in `requirements.txt`

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/spirteque/weather_e2e.git
   cd weather_e2e
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv ./venv
   source venv/bin/activate # Linux/macOS
   venv\Scripts\activate # Windows
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Tests Description

The tests cover the following functionalities of the Weather Application:

- **Automated Location**

  - If permission is granted,  fields in "Your Location" component are automatically filled.
  - If not, they should be filled with `0`.

- **Week Forecast Table**

  - Validation of table headers and rows (e.g., days of the week, temperature, energy values).
  - Verification of correct rendering after user input for location updates.

- **Week Summary Section**

  - Validation of displayed data (e.g., max/min temperatures, average pressure, sunshine duration, weather descriptions).
  - Checking for SVG icons and their correctness.

- **Location Inputs**

  - Tests for behavior when valid and invalid latitude/longitude inputs are provided.

- **User Interaction**

  - Tests to verify UI changes (or lack of changes) based on user interactions, such as clicking the "Update Location" button.

## Running the Tests

1. Start the Weather Application frontend on `localhost:3000` or a similar local environment.

2. Run all tests:

   ```bash
   pytest
   ```

3. Run a specific test:

   ```bash
   pytest tests/test_week_forecast.py::test_display_week_forecast_table
   ```

### Additional Notes

- Make sure the [frontend](https://github.com/spirteque/weather_frontend) is running before executing the tests (and .env file is updated accordingly).
- Some tests require valid or invalid geolocation permissions to simulate user scenarios. The fixtures `driver_with_location_permission` and `driver_without_location_permission` are used for this purpose.


### Browser Compatibility

   - Currently, the tests are configured to run on Google Chrome. Support for other browsers (e.g., Firefox) requires additional setup.

