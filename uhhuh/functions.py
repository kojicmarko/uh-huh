import datetime
from urllib.parse import urlparse
import re
import requests
from bs4 import BeautifulSoup
import numpy as np


def get_sec(time):
    """Get seconds from time string."""
    h, m, s = [int(t) for t in time.split(':')]
    return datetime.timedelta(hours=h, minutes=m, seconds=s).total_seconds()


def get_time_str(seconds):
    """Get time string from seconds."""
    return str(datetime.timedelta(seconds=seconds)).split('.')[0]


def get_table_name(url):
    """Convert URL to SQL table name."""
    name = 'E'
    for e in urlparse(url).path.split('/'):
        if len(e) == 1:
            name += e
        if e.isnumeric():
            name += e
    return name


def is_time(time):
    """Validate time input."""
    reg = re.compile(r'\b\d{1}[:]\d{2}[:]\d{2}\b')
    return reg.search(time)


def is_url(url):
    """Validate URL input."""
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    h1 = str(soup.select('h1')[0])
    table_exists = h1 != '<h1>You are asking too much questions!!!</h1>'
    reg = re.compile(
        r'^\bhttps:\/\/trka\.rs\/results\/\d{3,4}\/gender\/(M|F)\/$')

    return table_exists and bool(reg.search(url))


def get_runners(url, race_name):
    """Returns a list of tuples with runner data."""
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    runners = [tuple([race_name]) + tuple([td.text.strip() for td in tr.select('td')])
               for tr in soup.select('tr')[1:]]
    return runners


def crunch_the_numbers(gun_times, usr_time):
    """Crunch running times."""
    gun_times = [get_sec(time) for time in gun_times]

    deciles = list(np.percentile(gun_times, np.arange(0, 100, 10)))

    times_below_usr_time = [
        time for time in gun_times if time < get_sec(usr_time)]

    percentile_faster = round(100 -
                              (len(times_below_usr_time) / len(gun_times) * 100), 2)

    numbers_dict = {}
    numbers_dict['faster_than'] = percentile_faster
    numbers_dict['median'] = get_time_str(np.median(gun_times))
    numbers_dict['average'] = get_time_str(np.mean(gun_times))
    numbers_dict['first'] = get_time_str(deciles[0])
    numbers_dict['deciles'] = [get_time_str(time)
                               for time in deciles if time != deciles[0]]

    return numbers_dict
