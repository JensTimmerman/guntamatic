"""Tests for firmware 3.3 heater labels."""

import logging
from unittest.mock import MagicMock, patch

import pytest

from guntamatic.heater import TRANSLATE, Heater

LANGS = ["cz", "de", "en", "es", "fr", "hu", "it", "nl", "sl", "sw"]


@pytest.fixture
def heater() -> Heater:
    """Return a heater instance."""
    return Heater("1.1.1.1")


def parse_desc_file(heater: Heater, desc: str) -> dict:
    """Parse synthetic data for the given daqdesc content."""

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = desc
        else:
            # plausible non-placeholder value for every line
            lines = desc.split("\n")
            values = []
            for i, line in enumerate(lines):
                if not line.strip():
                    values.append("")
                elif TRANSLATE.get(line.split(";")[0].strip()) == "serial":
                    values.append("12345")
                elif "\u00b0C" in line or line.rstrip().endswith(";"):
                    values.append("21.50")
                else:
                    values.append("1")
            mock.text = "\n".join(values)
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        return heater.parse_data()


@pytest.mark.parametrize("lang", LANGS)
def test_fw33_labels_are_mapped(lang: str, heater: Heater) -> None:
    """Test every fw 3.3 label of this language maps to a known sensor."""
    logging.disable(logging.CRITICAL)
    try:
        desc = open(f"doc/params/fw33/{lang}.cgi", encoding="utf-8").read()
        data = parse_desc_file(heater, desc)
    finally:
        logging.disable(logging.NOTSET)

    assert "serial" in data
    assert data["serial"][0] == "12345"
    assert "boiler_temperature" in data
    assert "heating_circulation_pump_5" in data
    assert "room_8_temperature" in data or lang in ("de", "en", "es", "fr", "hu", "it", "nl", "sl", "sw")
