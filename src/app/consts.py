from enum import Enum
import datetime as dt

SUCCESS_MSG_COLOR = "green"
ALERT_MSG_COLOR = "orange"
ERROR_MSG_COLOR = "red"
CHART_RNG_INTERVALS = {
    '1 Minute' : '1m',
    '2 Minutes' : '2m',
    '5 Minutes' : '5m',
    '15 Minutes' : '15m',
    '30 Minutes' : '30m',
    '60 Minutes' : '60m',
    '90 Minutes' : '90m',
    '1 Hour' : '1h',
    '4 Hours' : '4h',
    '1 Day' : '1d',
    '5 Days' : '5d',
    '1 Week' : '1wk',
    '1 Month' : '1mo'
}
__today = dt.date.today()
TODAY_STR = __today.strftime("%Y-%m-%d")
THIRTY_DAYS_AGO_STR = (__today - dt.timedelta(days=60)).strftime("%Y-%m-%d")
PHI = 1.618033988749895 # Golden ratio

def golden_expand(x, factor=1):
    return x * PHI * factor

def golden_shrink(x, factor=1):
    return x / (PHI * factor)


class Font:
    TF = "Arial"
    H1 = 24
    H2 = 20
    TEXT = 18
    ENTRY_TEXT = 14
    BUTTON_TEXT = 18
    COMBO_TEXT = ENTRY_TEXT
    SUBTLE = 12


