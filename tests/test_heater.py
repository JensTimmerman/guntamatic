"""Tests for the Guntamatic heater module."""
from unittest.mock import MagicMock, patch
import pytest
from guntamatic.heater import Heater, NoSerialException

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

def mock_serial_get(url: str, **kwargs) -> MagicMock:
    """Return mock response based on URL."""
    mock = MagicMock()
    if "daqdesc" in url:
        mock.text = "Serial;\nVersion;\nreserved;°C\nProgram;\n;\n"
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

@patch("guntamatic.heater.requests.get", side_effect=mock_serial_get)
def test_get_data(mock_requests, heater: Heater) -> None:
    """Test get_data returns correct structure and translation."""
    data = heater.parse_data()
    print(data)
    assert data == {
        'serial': ['14.09', ''],
        'version': ['15.95', ''],
        'program': ['heat', ''],
    }

@patch("guntamatic.heater.requests.get", side_effect=mock_get)
def test_noserial_parse_data(mock_requests, heater: Heater) -> None:
    """Test parse_data raises exception when no serial present."""
    try:
        data = heater.parse_data()
    except NoSerialException:
        pass
    else:
        assert False, "No serial was present but NoSerialException was not raised"

@patch("guntamatic.heater.requests.get", side_effect=mock_serial_get)
def test_version_in_parsedata(mock_requests, heater: Heater) -> None:
    """Test parse_data raises exception when no serial present."""
    data = heater.parse_data()
    assert 'version' in data


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

def test_missing_dhw_pump_when_dhw_temp_60(heater: Heater) -> None:
    """Test that missing dhw_pump_1 doesn't give issues when dhw 1 is the default 60 degrees"""
    mock_desc = "Serial;\nDHW 1;°C\nDHW Pump 0;%\n"
    mock_data = "a\n60.00\n0\n"

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = mock_desc
        else:
            mock.text = mock_data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert "dhw_pump_1" not in data
