"""Tests for the Guntamatic heater module."""
from unittest.mock import MagicMock, patch
import pytest
from guntamatic.heater import Heater

MOCK_DESC = "Boiler temperature;°C\nOutside Temp.;°C\nreserved;°C\nProgram;\n;\n"
MOCK_DATA = "14.09\n15.95\n0\nHEAT\n\n"


@pytest.fixture
def heater() -> Heater:
    """Return a heater instance."""
    return Heater("1.1.1.1")


def mock_get(url: str, **kwargs) -> MagicMock:
    """Return mock response based on URL."""
    mock = MagicMock()
    if "daqdesc" in url:
        mock.text = MOCK_DESC
    else:
        mock.text = MOCK_DATA
    return mock


@patch("guntamatic.heater.requests.get", side_effect=mock_get)
def test_get_data(mock_requests, heater: Heater) -> None:
    """Test get_data returns correct structure."""
    data = heater.get_data()
    assert data == {
        "Boiler temperature": ["14.09", "°C"],
        "Outside Temp.": ["15.95", "°C"],
        "Program": ["HEAT", ""],
    }


@patch("guntamatic.heater.requests.get", side_effect=mock_get)
def test_get_data_skips_reserved(mock_requests, heater: Heater) -> None:
    """Test that reserved entries are skipped."""
    data = heater.get_data()
    assert not any("reserved" in key for key in data)


@patch("guntamatic.heater.requests.get", side_effect=mock_get)
def test_get_data_skips_empty_keys(mock_requests, heater: Heater) -> None:
    """Test that empty keys are skipped."""
    data = heater.get_data()
    assert "" not in data


def test_heater_init(heater: Heater) -> None:
    """Test heater initializes with correct attributes."""
    assert heater.host == "1.1.1.1"
    assert heater.protocol == "http://"
    assert heater.descurl == "daqdesc.cgi"
    assert heater.dataurl == "daqdata.cgi"
