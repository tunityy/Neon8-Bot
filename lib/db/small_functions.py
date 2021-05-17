import pytz
import datetime
from datetime import datetime, timezone
from string import capwords


def basic_listifier(item):
    """Takes strings, tuples, and lists of letters and/or numbers separated by spaces, with and without commas, and returns them in a neat and tidy list (without commas attached at the end."""
    if type(item) == tuple or type(item) == list:
        final = [x.replace(',','') for x in item]
        return final
    elif type(item) == str:
        final = [x.replace(',','') for x in item.split(' ')]
        return final


def timestamp_mountain():
    '''Return formatted timestamps, one in UTC, and one in MST/MDT'''
    aware_utc = datetime.now(timezone.utc)
    utc_ts = aware_utc.strftime("%Y-%m-%d %H:%M %Z")
    mountain = pytz.timezone('Canada/Mountain')
    local = mountain.localize(datetime.now())
    local_ts = local.strftime("%Y-%m-%d %H:%M %Z")
    return utc_ts, local_ts


def extra_spacing(number:int=1):
    lst = ['\U000E0020' for x in range(number)]
    spacey = ' '.join(lst)
    return spacey