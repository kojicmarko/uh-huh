import requests
from bs4 import BeautifulSoup
import zipfile
import io

#


def get_soup(url):
    res = requests.get(url)
    return BeautifulSoup(res.text, 'html.parser')


def event_href_to_event_url(event_href):
    return f"https://trka.rs{event_href}"


def event_href_to_results_url(event_href):
    event = event_href.split('/')
    event.insert(1, 'organizer')
    event.insert(-1, 'results')
    event.insert(-1, '_download-detailed-results')
    return f"https://trka.rs{'/'.join(event)}"


def get_races(races):
    return [race.find('a').text for race in races]


def get_dir_name(header):
    return header.split('filename=')[1].split('.zip')[0]

#


url = 'https://trka.rs/events/past/'

soup = get_soup(url)

events = [(event_href_to_event_url(event.find('a').get('href')), event_href_to_results_url(event.find('a').get('href')))
          for event in soup.find_all('div', class_='event-list-item') if event.find('div', class_='event-list-item-results').find('ul')]

for i, event in enumerate(events):
    event_soup = get_soup(event[0])

    races = get_races(event_soup.find_all('li', class_='list-group-item'))

    event_name = event_soup.find('div', class_='event-title').text.strip()

    res = requests.get(event[1])

    dir_name = get_dir_name(res.headers["Content-Disposition"])

    z = zipfile.ZipFile(io.BytesIO(res.content))

    z.extractall(f'event_results/i{i + 1}-{dir_name}/')

    with open(f'event_results/i{i + 1}-{dir_name}/races', 'w') as f:
        f.write(f'{event_name}\n')
        for race in races:
            f.write(f'{race}\n')
