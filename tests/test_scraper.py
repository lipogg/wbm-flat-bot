import pytest
from pathlib import Path
from wbmbot import Flat, FlatScraper


# flat summary attributes from flats.html
mock_attributes = [
    {
        "title": "2-Zimmer-Wohnung in Spandau",
        "total_rent": "1.161,35 €",
        "size": "55,49 m²",
        "rooms": "2",
        "zip_code": "13587",
        "property_attrs": ["Bad mit Wanne", "Aufzug", "Offene Küche", "Balkon", "Abstellraum"],
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/2-zimmer-wohnung-in-spandau-1/"
    },
    {
        "title": "4-Zimmer-Wohnung in Spandau",
        "total_rent": "1.693,95 €",
        "size": "96,07 m²",
        "rooms": "4",
        "zip_code": "13587",
        "property_attrs": ["Bad mit Wanne", "Aufzug", "Offene Küche", "Balkon"],
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-spandau-1/"
    },
    {
        "title": "4-Zimmer-Wohnung in Mitte",
        "total_rent": "1.012,34 €",
        "size": "100,90 m²",
        "rooms": "4",
        "zip_code": "10117",
        "property_attrs": ["Bad mit Wanne", "Aufzug", "barrierearm", "Balkon", "Abstellraum"],
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-mitte-1/"
    }
]

@pytest.fixture
def mock_attributes_fixture():
    return mock_attributes

@pytest.fixture
def flat_scraper(mocker):
    driver = mocker.Mock()
    start_url = "file://" + str((Path(__file__).parent / "data" / "flats.html").absolute())
    return FlatScraper(driver=driver, start_url=start_url)

def test_load_start_page(mocker, flat_scraper):
    html_path = Path(__file__).parent / "data" / "flats.html"
    html_string = html_path.read_text(encoding="utf-8")

    mocker.patch.object(flat_scraper, "_accept_cookies")
    mocker.patch.object(flat_scraper, "_scroll_to_footer")

    flat_scraper.driver.get.return_value = None  # get() returns nothing
    flat_scraper.driver.page_source = html_string

    result = flat_scraper.load_start_page()

    flat_scraper.driver.get.assert_called_once_with(flat_scraper.start_url)
    flat_scraper._accept_cookies.assert_called_once()
    flat_scraper._scroll_to_footer.assert_called_once()
    assert result == html_string

@pytest.mark.parametrize("mocked_return, expected_return", [
    (mock_attributes[0], mock_attributes[0]),
    (mock_attributes[1], mock_attributes[1]),
    (mock_attributes[2], mock_attributes[2]),
])
def test_get_summary_attributes(mocker, flat_scraper, mocked_return, expected_return):
    mock_extract_attributes = mocker.patch("wbmbot.scraper.FlatScraper._extract_summary_attributes", return_value=mocked_return)
    return_value = flat_scraper._extract_summary_attributes()

    mock_extract_attributes.assert_called_once()
    assert return_value == expected_return

def test_get_flats(mocker, flat_scraper, mock_attributes_fixture):
    fake_elems = [mocker.Mock() for _ in mock_attributes_fixture]
    mocker.patch.object(flat_scraper.driver, "find_elements", return_value=fake_elems)
    mocker.patch.object(flat_scraper, "_extract_summary_attributes", side_effect=mock_attributes_fixture)
    expected_flats = [Flat(mock_attr) for mock_attr in mock_attributes_fixture]
    returned_flats = flat_scraper.get_flats()

    # make Flats dataclass and change this to expected_flats == flats
    for expected, returned in zip(expected_flats, returned_flats):
        assert expected.__dict__ == returned.__dict__

# add test for no_flats.html