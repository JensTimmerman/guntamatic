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
        mock.text = "Serial;\nOutside Temp.;°C\nreserved;°C\nProgram;\n;\n"
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
        'status': None,
        'boiler_temperature': None,
        'outdoor_temperature': ['15.95', '°C'],
        'buffer_load': None,
        'buffer_top_temperature': None,
        'buffer_center_temperature': None,
        'buffer_bottom_temperature': None,
        'room_0_temperature': None,
        'room_1_temperature': None,
        'room_2_temperature': None,
        'program': ['heat', ''],
        'serial':  ['14.09', ''],
        'version': None,
        'boiler_shunt_pump': None,
        'circuit_0_temp': None,
        'circuit_1_temp': None,
        'circuit_2_temp': None,
        'circuit_3_temp': None,
        'circuit_4_temp': None,
        'circuit_5_temp': None,
        'circuit_6_temp': None,
        'circuit_7_temp': None,
        'circuit_8_temp': None,
        'co2_content': None,
        'dhw_pump_0': None,
        'dhw_pump_1': None,
        'dhw_pump_2': None,
        'domestic_hot_water_0_temperature': None,
        'domestic_hot_water_1_temperature': None,
        'domestic_hot_water_2_temperature': None,
        'heating_circulation_program_0': None,
        'heating_circulation_program_1': None,
        'heating_circulation_program_2': None,
        'heating_circulation_program_3': None,
        'heating_circulation_program_4': None,
        'heating_circulation_program_5': None,
        'heating_circulation_program_6': None,
        'heating_circulation_program_7': None,
        'heating_circulation_program_8': None,
        'heating_circulation_pump_0': None,
        'heating_circulation_pump_1': None,
        'heating_circulation_pump_2': None,
        'heating_circulation_pump_3': None,
        'heating_circulation_pump_4': None,
        'heating_circulation_pump_5': None,
        'heating_circulation_pump_6': None,
        'heating_circulation_pump_7': None,
        'heating_circulation_pump_8': None,
        'primary_air': None,
        'room_3_temperature': None,
        'room_4_temperature': None,
        'room_5_temperature': None,
        'room_6_temperature': None,
        'room_7_temperature': None,
        'room_8_temperature': None,
        'secondary_air': None,
        'suction_fan': None
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
