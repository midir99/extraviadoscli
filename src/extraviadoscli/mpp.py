import dataclasses
import datetime
import enum


class StateChoices(enum.Enum):
    CIUDAD_DE_MEXICO = "MX-CMX"
    AGUASCALIENTES = "MX-AGU"
    BAJA_CALIFORNIA = "MX-BCN"
    BAJA_CALIFORNIA_SUR = "MX-BCS"
    CAMPECHE = "MX-CAM"
    COAHUILA_DE_ZARAGOZA = "MX-COA"
    COLIMA = "MX-COL"
    CHIAPAS = "MX-CHP"
    CHIHUAHUA = "MX-CHH"
    DURANGO = "MX-DUR"
    GUANAJUATO = "MX-GUA"
    GUERRERO = "MX-GRO"
    HIDALGO = "MX-HID"
    JALISCO = "MX-JAL"
    MEXICO = "MX-MEX"
    MICHOACAN_DE_OCAMPO = "MX-MIC"
    MORELOS = "MX-MOR"
    NAYARIT = "MX-NAY"
    NUEVO_LEON = "MX-NLE"
    OAXACA = "MX-OAX"
    PUEBLA = "MX-PUE"
    QUERETARO = "MX-QUE"
    QUINTANA_ROO = "MX-ROO"
    SAN_LUIS_POTOSI = "MX-SLP"
    SINALOA = "MX-SIN"
    SONORA = "MX-SON"
    TABASCO = "MX-TAB"
    TAMAULIPAS = "MX-TAM"
    TLAXCALA = "MX-TLA"
    VERACRUZ_DE_IGNACIO_DE_LA_LLAVE = "MX-VER"
    YUCATAN = "MX-YUC"
    ZACATECAS = "MX-ZAC"


class PhysicalBuildChoices(enum.Enum):
    SLIM = "S"
    REGULAR = "R"
    HEAVY = "H"


class ComplexionChoices(enum.Enum):
    VERY_LIGHT = "VL"
    LIGHT = "L"
    LIGHT_INTERMEDIATE = "LI"
    DARK_INTERMEDIATE = "DI"
    DARK = "D"
    VERY_DARK = "VD"


class SexChoices(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class AlertTypeChoices(enum.Enum):
    ALBA = "AL"
    AMBER = "AM"
    HAS_VISTO_A = "HV"
    ODISEA = "OD"


@dataclasses.dataclass
class MissingPersonPoster:
    mp_name: str
    mp_height: int | None = None
    mp_weight: int | None = None
    mp_physical_build: str = ""
    mp_complexion: str = ""
    mp_sex: str = ""
    mp_dob: datetime.date | None = None
    mp_age_when_disappeared: int | None = None
    mp_eyes_description: str = ""
    mp_hair_description: str = ""
    mp_outfit_description: str = ""
    mp_identifying_characteristics: str = ""
    circumstances_behind_dissapearance: str = ""
    missing_from: str = ""
    missing_date: datetime.date | None = None
    found: bool = False
    alert_type: str = ""
    po_state: str = ""
    po_post_url: str = ""
    po_post_publication_date: datetime.date | None = None
    po_poster_url: str = ""
    is_multiple: bool = False
