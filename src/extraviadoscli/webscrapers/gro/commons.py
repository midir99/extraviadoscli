from ... import mpp


def parse_found(found_raw: str) -> bool:
    found_raw = found_raw.strip().lower()
    return bool({"localizada", "localizado"}.intersection({found_raw}))


def parse_po_poster_url(po_poster_url_raw: str) -> str:
    return (
        po_poster_url_raw.replace("background-image: url(&quot;", "")
        .replace("&quot;);", "")
        .replace("-480x320", "")
    )


def parse_sex(found_raw: str) -> str:
    found_raw = found_raw.strip().lower()
    if found_raw in {"localizada", "desaparecida"}:
        return mpp.SexChoices.FEMALE.value
    if found_raw in {"localizado", "desaparecido"}:
        return mpp.SexChoices.MALE.value
    return ""
