"""API client for Voxnet."""

from __future__ import annotations

import logging

import requests
from bs4 import BeautifulSoup

from .const import SELECTOR, URL

_LOGGER = logging.getLogger(__name__)


class VoxnetApiError(Exception):
    """Base Voxnet API error."""


class VoxnetClient:
    """Small synchronous client for the Voxnet balance page."""

    def __init__(self, login: str, password: str) -> None:
        self._login = login
        self._password = password

    def get_balance(self) -> float:
        """Fetch and parse balance from Voxnet."""
        payload = {
            "login": self._login,
            "password": self._password,
        }

        try:
            response = requests.post(URL, data=payload, timeout=20)
            response.raise_for_status()
        except requests.RequestException as err:
            raise VoxnetApiError(f"Request failed: {err}") from err

        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select(SELECTOR)

        if not elements:
            _LOGGER.debug("Balance selector was not found in Voxnet response")
            raise VoxnetApiError("Balance selector was not found")

        raw = elements[0].text.split("\xa0")[0].strip().replace(",", ".")

        try:
            return round(float(raw), 2)
        except ValueError as err:
            raise VoxnetApiError(f"Could not parse balance value: {raw!r}") from err
