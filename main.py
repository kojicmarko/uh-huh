import sys
import requests
from bs4 import BeautifulSoup
from helpers import lst_to_csv_str
import cyrtranslit

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

res = requests.get(sys.argv[1])

soup = BeautifulSoup(res.text, 'html.parser')

headers = [cyrtranslit.to_latin(th.text) for th in soup.select('th')]

rows = [[td.text.strip() for td in rows.select('td')]
        for rows in soup.select('tr')[1:]]

with open('trka.csv', 'w') as f:
    f.write(lst_to_csv_str(headers))
    for row in rows:
        # print(cyrtranslit.to_latin(repr(lst_to_csv_str(row))))
        f.write(cyrtranslit.to_latin(lst_to_csv_str(row)))
