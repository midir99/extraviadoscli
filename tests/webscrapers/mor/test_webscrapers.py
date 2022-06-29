import datetime
import pathlib

import bs4
import pytest

from extraviadoscli import mpp
from extraviadoscli.webscrapers import mor, utils


def file2soup(filepath):
    with open(filepath, "rt", encoding="utf-8") as file:
        html = file.read()
    return bs4.BeautifulSoup(html, "html.parser")


class TestAmberAlertWebScraper:
    @pytest.fixture
    def ws(self):
        return mor.AmberAlertWebScraper()

    @pytest.fixture
    def post_1(self):
        filepath = pathlib.Path(__file__).parent / "html/amber_post_1.html"
        return file2soup(filepath)

    @pytest.fixture
    def article_1(self):
        filepath = pathlib.Path(__file__).parent / "html/amber_article_1.html"
        return file2soup(filepath)

    @pytest.fixture
    def full_page_1(self):
        filepath = pathlib.Path(__file__).parent / "html/amber_full_page_1.html"
        return file2soup(filepath)

    @pytest.mark.parametrize(
        "page,expected",
        [
            (32, "https://fiscaliamorelos.gob.mx/category/alerta-amber/page/32/"),
            (41, "https://fiscaliamorelos.gob.mx/category/alerta-amber/page/41/"),
            (20, "https://fiscaliamorelos.gob.mx/category/alerta-amber/page/20/"),
        ],
    )
    def test_make_url(self, ws, page, expected):
        result = ws.make_url(page)
        assert result == expected

    def test_extract_po_poster_url(self, monkeypatch, ws, post_1):
        def mock_retrieve_from_soup(page_url):
            return post_1

        monkeypatch.setattr(utils, "retrieve_soup_from", mock_retrieve_from_soup)
        result = ws.extract_po_poster_url(None)
        assert (
            "https://fiscaliamorelos.gob.mx/wp-content/uploads/2020/08/PEYTHON-NICOL-"
            "FÚNEZ-MURILLO.jpg"
        ) == result

    def test_extract_mpp_data_from_html(self, monkeypatch, ws, article_1, post_1):
        def mock_retrieve_from_soup(page_url):
            return post_1

        monkeypatch.setattr(utils, "retrieve_soup_from", mock_retrieve_from_soup)
        result = ws.extract_mpp_data_from_html(article_1)
        assert {
            "mp_name": "Peython Nicol Fúnez Murillo",
            "po_post_url": "https://fiscaliamorelos.gob.mx/2020/08/28/peython-nicol-funez-murillo/",
            "po_post_publication_date": datetime.date(2020, 8, 28),
            "po_poster_url": "https://fiscaliamorelos.gob.mx/wp-content/uploads/2020/08/PEYTHON-NICOL-FÚNEZ-MURILLO.jpg",
            "alert_type": mpp.AlertTypeChoices.AMBER.value,
            "po_state": mpp.StateChoices.MORELOS.value,
        } == result

    def test_extract_mpps_in_html(self, monkeypatch, ws, full_page_1):
        def mock_retrieve_from_soup(page_url):
            return full_page_1

        monkeypatch.setattr(utils, "retrieve_soup_from", mock_retrieve_from_soup)
        articles = ws.extract_mpps_in_html(None)
        assert len(articles) == 10


class TestCustomAlertWebScraper:
    @pytest.fixture
    def ws(self):
        return mor.CustomAlertWebScraper()

    @pytest.fixture
    def article_1(self):
        filepath = pathlib.Path(__file__).parent / "html/custom_article_1.html"
        return file2soup(filepath)

    @pytest.fixture
    def full_page_1(self):
        filepath = pathlib.Path(__file__).parent / "html/custom_full_page_1.html"
        return file2soup(filepath)

    @pytest.mark.parametrize(
        "page,expected",
        [
            (1, "https://fiscaliamorelos.gob.mx/cedulas/1/"),
            (53, "https://fiscaliamorelos.gob.mx/cedulas/53/"),
            (40, "https://fiscaliamorelos.gob.mx/cedulas/40/"),
        ],
    )
    def test_make_url(self, ws, page, expected):
        result = ws.make_url(page)
        assert result == expected

    def test_extract_mpp_data_from_html(self, ws, article_1):
        result = ws.extract_mpp_data_from_html(article_1)
        assert {
            "mp_name": "Zuri Saray Tapia Díaz",
            "po_post_url": "https://fiscaliamorelos.gob.mx/2020/12/14/zuri-saray-tapia-diaz/",
            "po_post_publication_date": datetime.date(2020, 12, 14),
            "po_poster_url": "https://fiscaliamorelos.gob.mx/wp-content/uploads/2020/12/ZURI-SARAY-TAPIA-DIAZ.jpeg",
            "alert_type": "",
            "po_state": mpp.StateChoices.MORELOS.value,
        } == result

    def test_extract_mpps_in_html(self, monkeypatch, ws, full_page_1):
        def mock_retrieve_from_soup(page_url):
            return full_page_1

        monkeypatch.setattr(utils, "retrieve_soup_from", mock_retrieve_from_soup)
        articles = ws.extract_mpps_in_html(None)
        assert len(articles) == 6
