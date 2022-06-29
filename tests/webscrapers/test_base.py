import dataclasses
import datetime

import bs4
import pytest

from extraviadoscli import mpp
from extraviadoscli.webscrapers import base


@pytest.mark.parametrize(
    "page_numbers,expected",
    [
        (
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10),
            "1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
        ),
        (
            (6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21),
            "6, 7, 8, ..., 19, 20, 21",
        ),
    ],
)
def test_humanize_pages(page_numbers, expected):
    result = base.humanize_pages(page_numbers)
    assert result == expected


@pytest.mark.parametrize(
    "page_from,page_to,expected",
    [
        (
            5,
            10,
            "5 -> 10",
        ),
        (
            8,
            12,
            "8 -> 12",
        ),
    ],
)
def test_humanize_page_range(page_from, page_to, expected):
    result = base.humanize_page_range(page_from, page_to)
    assert result == expected


def create_salomons_mpp_data():
    return {
        "mp_name": "Salomon",
        "mp_height": None,
        "mp_weight": None,
        "mp_physical_build": "",
        "mp_complexion": "",
        "mp_sex": mpp.SexChoices.MALE.value,
        "mp_dob": None,
        "mp_age_when_disappeared": None,
        "mp_eyes_description": "",
        "mp_hair_description": "",
        "mp_outfit_description": "",
        "mp_identifying_characteristics": "",
        "circumstances_behind_dissapearance": "",
        "missing_from": "",
        "missing_date": None,
        "found": False,
        "alert_type": "",
        "po_state": mpp.StateChoices.MORELOS.value,
        "po_post_url": "https://example.com",
        "po_post_publication_date": datetime.date(2022, 5, 27),
        "po_poster_url": "https://example.com",
        "is_multiple": False,
    }


class DummyWebScraper(base.PaginatedContentWebScraper):
    def make_url(self, page_number):
        return "https://example.com"

    def extract_mpp_data_from_html(self, soup):
        return create_salomons_mpp_data()

    def extract_mpps_in_html(self, page_url):
        return [
            bs4.BeautifulSoup("<html></html>", "html.parser"),
            bs4.BeautifulSoup("<html></html>", "html.parser"),
        ]


class TestPaginatedContentWebScraper:
    @pytest.fixture
    def ws(self):
        return DummyWebScraper()

    def test_scrap_page(self, ws):
        salomons_mpp_data = create_salomons_mpp_data()
        for result in ws.scrap_page(None):
            assert result == mpp.MissingPersonPoster(**salomons_mpp_data)

    def test_scrap_mpps_by_pages(self, ws):
        salomons_mpp_data = create_salomons_mpp_data()
        results = ws.scrap_mpps_by_pages([None, None])
        for result in results:
            assert result == mpp.MissingPersonPoster(**salomons_mpp_data)
        assert len(results) == 4

    def test_scrap_mpps_until_find_po_post_url(self, ws):
        salomons_mpp_data = create_salomons_mpp_data()
        results = ws.scrap_mpps_until_find_po_post_url(max_pages=0)
        assert results == []
        results = ws.scrap_mpps_until_find_po_post_url(post_url="https://example.com")
        assert len(results) == 1
        assert results[0] == mpp.MissingPersonPoster(**salomons_mpp_data)
        results = ws.scrap_mpps_until_find_po_post_url(
            post_url="U-will-never-find-me",
            max_pages=2,
        )
        assert len(results) == 4
