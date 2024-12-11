import random
import string
from datetime import datetime
from functools import wraps
from typing import Any, Callable

from selenium.common import NoSuchElementException, TimeoutException


def handle_exceptions(func: Callable[..., Any]) -> Callable[..., Any]:
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			return func(*args, **kwargs)

		except (TimeoutException, NoSuchElementException) as e:
			raise AssertionError(f"Could not find error messages: {str(e)}")

	return wrapper


def create_random_valid_float(latitude: bool = False, longitude: bool = False) -> float | None:
	if latitude:
		return round(random.uniform(-90, 90), 4)
	if longitude:
		return round(random.uniform(-180, 180), 4)

	return None


def create_random_invalid_float(latitude: bool = False, longitude: bool = False) -> float | None:
	if latitude:
		random_minus_latitude_value = str(round(random.uniform(-1000, -90.0001), 4))
		random_plus_latitude_value = str(round(random.uniform(90.0001, 1000), 4))
		return random.choice([random_minus_latitude_value, random_plus_latitude_value])

	if longitude:
		random_minus_longitude_value = str(round(random.uniform(-1000, -180.0001), 4))
		random_plus_longitude_value = str(round(random.uniform(180.0001, 1000), 4))
		return random.choice([random_minus_longitude_value, random_plus_longitude_value])

	return None


def create_random_non_float(length: int = 10) -> str:
	allowed_chars = string.ascii_letters + string.punctuation + string.digits
	while True:
		result = ''.join(random.choices(allowed_chars, k=length))
		if not result.replace('.', '').isdigit():
			return result


def get_dynamic_days_order() -> list[str]:
	days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
	today = datetime.now().weekday()
	return days[today:] + days[:today]
