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


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # english
        ("OFF", "off"),
        ("TIMER", "timer"),
        ("HEAT", "heat"),
        ("HIBERNAT", "hibernate"),
        ("HIBERNATE TO", "hibernate_to"),
        # spanish
        ("normal", "timer"),
        ("CALENTAR", "heat"),
        ("Reducido hasta", "hibernate_to"),
        # german
        ("Aus", "off"),
        ("Absenken bis", "hibernate_to"),
        # french
        ("DIMIN.", "hibernate"),
        ("DIMIN.JUSQ.", "hibernate_to"),
        # italian
        ("NORMALE", "timer"),
        ("RIDUR", "hibernate"),
        # czech
        ("VYPNUTO", "off"),
        ("UTLUM DO", "hibernate_to"),
        # slovenian
        ("IZKLOP", "off"),
        ("Znizaj do", "hibernate_to"),
        # hungarian
        ("KI", "off"),
        ("Csökkent -ig", "hibernate_to"),
        # dutch
        ("Uit", "off"),
        ("Reduceren tot", "hibernate_to"),
    ],
)
def test_heating_circulation_program_translation(
    heater: Heater, value: str, expected: str
) -> None:
    """Test heating circulation program values are translated from every language."""
    mock_desc = "Serial;\nProgram HC0;\n"
    mock_data = f"a\n{value}\n"

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = mock_desc
        else:
            mock.text = mock_data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["heating_circulation_program_0"][0] == expected


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        # english
        ("AUTO", "auto"),
        ("OFF", "off"),
        ("NONSTP", "nonstop"),
        # spanish
        ("Auto", "auto"),
        ("Off", "off"),
        ("DURACIÓN", "nonstop"),
        # german
        ("AUS", "off"),
        ("DAUER", "nonstop"),
        # french
        ("DUREE", "nonstop"),
        # italian
        ("CONTIN", "nonstop"),
        # czech
        ("VYP", "off"),
        ("TRVALE", "nonstop"),
        # slovenian
        ("AVTO", "auto"),
        ("IZKKLOP", "off"),  # typo present in slovenian firmware
        ("TRAJNO", "nonstop"),
        # hungarian
        ("KI", "off"),
        ("TARTÓS", "nonstop"),
        # dutch
        ("uit", "off"),
        ("Continue", "nonstop"),
    ],
)
def test_pump_mode_translation(heater: Heater, value: str, expected: str) -> None:
    """Test pump operating mode values are translated from every language."""
    for key, translated_key in (
        ("Heating circulation pump 0", "heating_circulation_pump_0"),
        ("Auxiliary pump 0", "auxiliary_pump_0"),
    ):
        mock_desc = f"Serial;\n{key};\n"
        mock_data = f"a\n{value}\n"

        def mock_get(url: str, mock_desc=mock_desc, mock_data=mock_data, **kwargs) -> MagicMock:
            mock = MagicMock()
            if "daqdesc" in url:
                mock.text = mock_desc
            else:
                mock.text = mock_data
            return mock

        with patch("guntamatic.heater.requests.get", side_effect=mock_get):
            data = heater.parse_data()

        assert data[translated_key][0] == expected


def test_unknown_enum_value_passes_through(heater: Heater) -> None:
    """Test that unknown enum values are passed through untranslated."""
    mock_desc = "Serial;\nProgram HC0;\nHeating circulation pump 0;\n"
    mock_data = "a\nNONSENSE\nALSO NONSENSE\n"

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = mock_desc
        else:
            mock.text = mock_data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["heating_circulation_program_0"][0] == "NONSENSE"
    assert data["heating_circulation_pump_0"][0] == "ALSO NONSENSE"


def test_percent_pumps_are_not_translated(heater: Heater) -> None:
    """Test that modulating pumps reported as percentages are left alone."""
    mock_desc = "Serial;\nDHW Pump 0;%\nBoil.shunt pump;%\n"
    mock_data = "a\n55.00\n12.00\n"

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = mock_desc
        else:
            mock.text = mock_data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["dhw_pump_0"] == ["55.00", "%"]
    assert data["boiler_shunt_pump"] == ["12.00", "%"]


def parse_with(heater: Heater, desc: str, data: str) -> dict:
    """Run parse_data against mocked desc/data payloads."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = desc
        else:
            mock.text = data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        return heater.parse_data()


def test_service_time_reported_in_days(heater: Heater) -> None:
    """Test service time in days is exposed as both days and hours."""
    data = parse_with(heater, "Serial;\nService Hrs;d\n", "a\n2012\n")
    assert data["service_days"] == ["2012", "d"]
    assert data["service_hours"] == ["48288", "h"]


def test_service_time_reported_in_hours(heater: Heater) -> None:
    """Test service time in hours is exposed as both hours and days."""
    data = parse_with(heater, "Serial;\nService Hrs;h\n", "a\n48\n")
    assert data["service_hours"] == ["48", "h"]
    assert data["service_days"] == ["2", "d"]


def test_service_time_unknown_unit_untouched(heater: Heater) -> None:
    """Test that an unrecognized unit is passed through without normalization."""
    data = parse_with(heater, "Serial;\nService Hrs;x\n", "a\n7\n")
    assert data["service_hours"] == ["7", "x"]
    assert "service_days" not in data


def test_service_time_non_numeric_untouched(heater: Heater) -> None:
    """Test that non-numeric service time values are left alone."""
    data = parse_with(heater, "Serial;\nService Hrs;d\n", "a\nN/A\n")
    assert data["service_hours"] == ["N/A", "d"]
    assert "service_days" not in data
