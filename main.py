import sys
import requests
from bs4 import BeautifulSoup
from helpers import lst_to_csv_str

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

res = requests.get(sys.argv[1])

soup = BeautifulSoup(res.text, 'html.parser')

rows = [[row.string for row in rows] for rows in soup.table.find_all('tr')]

with open('trka.csv', 'w') as f:
    for row in rows:
        f.write(lst_to_csv_str(row))
