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


def circuit_slot_parse(heater: Heater, room: str, flow: str) -> dict:
    """Parse a heater reporting the given room/flow temps for circuit 1."""
    desc = (
        "Serial;\nRoom Temp:HC 1;°C\nFlow is 1;°C\nHeating circulation pump 1;\n"
        "Program HC1;\nDHW 0;°C\nDHW Pump 0;%\n"
    )
    data = f"a\n{room}\n{flow}\nAUTO\nHEAT\n41.18\n0\n"

    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        mock.text = desc if "daqdesc" in url else data
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        return heater.parse_data()


@pytest.mark.parametrize("placeholder", ["49.0", "49.00", "-20.00", "60.00"])
def test_placeholder_flow_hides_circuit(heater: Heater, placeholder: str) -> None:
    """Test a placeholder flow temperature filters the whole circuit slot."""
    data = circuit_slot_parse(heater, "21.50", placeholder)
    assert "circuit_1_temp" not in data
    assert "heating_circulation_pump_1" not in data
    assert "heating_circulation_program_1" not in data
    assert data["room_1_temperature"] == ["21.50", "°C"]


@pytest.mark.parametrize("placeholder", ["49.0", "60.00"])
def test_placeholder_room_hides_circuit(heater: Heater, placeholder: str) -> None:
    """Test a placeholder room temperature filters the whole circuit slot."""
    data = circuit_slot_parse(heater, placeholder, "55.00")
    assert "room_1_temperature" not in data
    assert "circuit_1_temp" not in data
    assert "heating_circulation_pump_1" not in data
    assert "heating_circulation_program_1" not in data


def test_connected_circuit_is_kept(heater: Heater) -> None:
    """Test a connected circuit with real temperatures is kept."""
    data = circuit_slot_parse(heater, "21.50", "55.00")
    assert data["room_1_temperature"] == ["21.50", "°C"]
    assert data["circuit_1_temp"] == ["55.00", "°C"]
    assert data["heating_circulation_pump_1"][0] == "auto"
    assert data["heating_circulation_program_1"][0] == "heat"


def test_default_dhw_hides_dhw_slot(heater: Heater) -> None:
    """Test a default DHW temperature hides the DHW temperature and pump."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = "Serial;\nDHW 0;°C\nDHW Pump 0;%\n"
        else:
            mock.text = "a\n60.00\n0\n"
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert "domestic_hot_water_0_temperature" not in data
    assert "dhw_pump_0" not in data


def test_real_dhw_is_kept(heater: Heater) -> None:
    """Test a real DHW temperature is kept."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = "Serial;\nDHW 0;°C\nDHW Pump 0;%\n"
        else:
            mock.text = "a\n41.18\n35\n"
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["domestic_hot_water_0_temperature"] == ["41.18", "°C"]
    assert data["dhw_pump_0"] == ["35", "%"]


def test_realistic_buffer_temperature_is_kept(heater: Heater) -> None:
    """Test a realistic buffer temperature is not filtered as a placeholder."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = "Serial;\nBuffer Top;\u00b0C\nBuffer Btm;\u00b0C\n"
        else:
            mock.text = "a\n49.0\n44.5\n"
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["buffer_top_temperature"] == ["49.0", "\u00b0C"]
    assert data["buffer_bottom_temperature"] == ["44.5", "\u00b0C"]


def test_default_buffer_stage_is_filtered(heater: Heater) -> None:
    """Test absent buffer stages at their placeholder value are filtered."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = "Serial;\nBuffer Top 0;\u00b0C\nBuffer Top 1;\u00b0C\n"
        else:
            mock.text = "a\n120.00\n55.00\n"
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert "buffer_top_0_temperature" not in data
    assert data["buffer_top_1_temperature"] == ["55.00", "\u00b0C"]


@pytest.mark.parametrize("boiler_temp", ["43.00", "44.00", "49.00"])
def test_boiler_temperature_is_never_filtered(
    heater: Heater, boiler_temp: str
) -> None:
    """Test boiler temperatures are kept even when matching placeholder values."""
    def mock_get(url: str, **kwargs) -> MagicMock:
        mock = MagicMock()
        if "daqdesc" in url:
            mock.text = "Serial;\nBoiler temperature;\u00b0C\n"
        else:
            mock.text = f"a\n{boiler_temp}\n"
        return mock

    with patch("guntamatic.heater.requests.get", side_effect=mock_get):
        data = heater.parse_data()

    assert data["boiler_temperature"] == [boiler_temp, "\u00b0C"]
