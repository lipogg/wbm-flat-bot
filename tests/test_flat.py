import pytest
from wbmbot import Flat, User

mock_user_config = {
    'email': 'johndoe@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'kw_filter': ['Balkon', 'Aufzug'],
    'loc_filter': ['10', '120', '121', '124', '1419', '140', '133'],
    'max_rent': '1300',
    'min_rooms': '2',
    'min_sqm': '50',
    'net_income': '4400',
    'wbs': 'no'
}

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

mock_detail_attributes = [
    {
        "base_rent": "400,45 EUR",
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/2-zimmer-wohnung-in-spandau-1/"
    },
    {
        "base_rent": "1.400,17 EUR",
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-spandau-1/"
    },
    {
        "base_rent": "900,20 EUR",
        "detail_url": "https://www.wbm.de/wohnungen-berlin/angebote/details/4-zimmer-wohnung-in-mitte-1/"
    }
]

@pytest.fixture
def mock_user_config_fixture():
    return mock_user_config

@pytest.fixture
def mock_attributes_fixture():
    return mock_attributes

@pytest.fixture
def user(mock_user_config_fixture):
    return User(attributes=mock_user_config_fixture)

@pytest.mark.parametrize("mocked_attribute, expected_return", [
    (mock_attributes[0], False),
    (mock_attributes[1], False),
    (mock_attributes[2], True),
])
def test_matches_criteria(user, mocked_attribute, expected_return):
    flat = Flat(attributes=mocked_attribute)
    return_value = flat.matches_criteria(user)
    assert return_value == expected_return

@pytest.mark.parametrize("mocked_attribute, mocked_detail_attribute, expected_return", [
    (mock_attributes[0], mock_detail_attributes[0], False),
    (mock_attributes[1], mock_detail_attributes[1], False),
    (mock_attributes[2], mock_detail_attributes[2], True),
])
def test_within_range(user, mocked_attribute, mocked_detail_attribute, expected_return):
    flat = Flat(attributes=mocked_attribute)
    flat.update_details(mocked_detail_attribute)
    return_value = flat.within_range(user)
    assert return_value == expected_return
