import datetime
import logging
from typing import Any

import bs4

from ... import mpp
from .. import base, utils
from . import commons


class AmberAlertWebScraper(base.PaginatedContentWebScraper):
    BASE_URL = "https://fiscaliaguerrero.gob.mx/category/amber/page"

    def make_url(self, page_number: int) -> str:
        return f"{self.BASE_URL}/{page_number}/"

    def extract_mpp_data_from_html(self, soup: bs4.BeautifulSoup) -> dict[str, Any]:
        mpp_data = {}
        try:
            data = soup.h2.a.get_text().strip()
            found_raw, mp_name = "", data
            seps = (";", ":", ",", ".")
            for sep in seps:
                data_list = data.split(sep)
                if len(data_list) >= 2:
                    found_raw, mp_name = (
                        data_list[0],
                        "".join(data_list[1:]).strip().title(),
                    )
                    break
            mpp_data["mp_name"] = mp_name.strip().title()
            try:
                mpp_data["mp_sex"] = commons.parse_sex(found_raw)
                mpp_data["found"] = commons.parse_found(found_raw)
            except Exception:
                logging.exception(
                    "unable to get the mp_sex or found from the div: %s", soup
                )
        except Exception as e:
            logging.exception(
                "unable to get the mp_name, mp_sex or found from the div: %s", soup
            )
            raise e

        try:
            mpp_data["po_post_url"] = soup.h2.a.get("href", "").strip()
        except Exception as e:
            logging.exception("unable to get the po_post_url from the div: %s", soup)
            raise e

        try:
            mpp_data["po_poster_url"] = (
                soup.a.get("data-src").strip().replace("-480x320", "")
            )
        except Exception:
            logging.exception("unable to get the po_poster_url from the div: %s", soup)
            mpp_data["po_poster_url"] = ""

        try:
            time_tag = soup.find(class_="entry-date published")
            if time_tag is None:
                time_tag = soup.find(class_="entry-date")
            date_raw = time_tag.get("datetime", "").split("T")[0]
            mpp_data["po_post_publication_date"] = datetime.datetime.strptime(
                date_raw, "%Y-%m-%d"
            ).date()
        except Exception as e:
            logging.exception(
                "unable to get the po_post_publication_date from the div: %s", soup
            )
            mpp_data["po_post_publication_date"] = None

        mpp_data["alert_type"] = mpp.AlertTypeChoices.AMBER.value
        mpp_data["po_state"] = mpp.StateChoices.GUERRERO.value
        return mpp_data

    def extract_mpps_in_html(self, page_url: str) -> list[bs4.BeautifulSoup]:
        soup = utils.retrieve_soup_from(page_url)
        return soup.find_all(class_="article_content")
