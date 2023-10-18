import sys
import requests
from bs4 import BeautifulSoup
from helpers import lst_to_csv_str
import cyrtranslit
import sqlite3
from urllib.parse import urlparse

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

url = sys.argv[1]

path = urlparse(url).path

con = sqlite3.connect('test.db')
cur = con.cursor()

cur.execute("INSERT INTO event (event) VALUES(?)", path)

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

headers = [cyrtranslit.to_latin(th.text) for th in soup.select('th')]

rows = [[td.text.strip() for td in rows.select('td')]
        for rows in soup.select('tr')[1:]]


# sql_headers = ['place', 'start_no', 'first_name', 'last_name',
#    'club', 'country', 'net_time', 'gross_time', 'status', 'remark']

# con = sqlite3.connect('test.db')
# cur = con.cursor()

# with open('test.sql') as f:
#     cur.executescript(f.read())
#     print('Initialized the database.')

# for row in rows:
#     cur.execute(
#         "INSERT INTO trka(place,start_no,first_name,last_name,club,country,net_time,gross_time,status,remark) VALUES(?,?,?,?,?,?,?,?,?,?)", (int(row[0]), int(row[1]), row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
#     con.commit()

# con.close()


# with open('test.csv', 'w') as f:
#     # f.write(lst_to_csv_str(headers))
#     for row in rows:
#         # print(row)
#         # print(cyrtranslit.to_latin(repr(lst_to_csv_str(row))))
#         f.write(cyrtranslit.to_latin(lst_to_csv_str(row)))
