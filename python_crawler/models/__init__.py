from enum import Enum


class BrowserType(Enum):
    CHROMIUM = 1, 'Chromium'
    FIREFOX = 1, 'Firefox'


class Location(Enum):
    """
        Feel free to add your languages if it's missing on the following list
    """

    WORLDWIDE = '.com'
    AUSTRALIA = '.au'
    BELGIUM = '.be'
    CANADA = '.ca'
    DENMARK = '.dk'
    FRANCE = '.fr'
    GERMANY = '.de'
    IRELAND = '.ie'
    ITALIA = '.it'
    NEW_ZEALAND = '.nz'
    SPAIN = '.es'
    SWITZERLAND = '.ch'