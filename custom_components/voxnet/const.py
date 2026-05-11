"""Constants for Voxnet integration."""

DOMAIN = "voxnet"

CONF_LOGIN = "login"
CONF_PASSWORD = "password"
CONF_ACCOUNT_NAME = "account_name"
CONF_SCAN_INTERVAL = "scan_interval"

# Интервал хранится и показывается в минутах.
DEFAULT_SCAN_INTERVAL = 60
MIN_SCAN_INTERVAL = 1

URL = "https://voxnet.lantek.ru/"
SELECTOR = "tr:nth-child(5) > td:nth-child(2) > p"

PLATFORMS = ["sensor", "button"]
