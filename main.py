import sys
import requests
from bs4 import BeautifulSoup
from helpers import get_table_name
import sqlite3

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

URL = sys.argv[1]
TABLE_NAME = get_table_name(URL)
CREATE_TABLE = f"""
CREATE TABLE {TABLE_NAME} (
  place INTEGER PRIMARY KEY,
  start_no INTEGER,
  first_name TEXT,
  last_name TEXT,
  club TEXT,
  country TEXT,
  net_time TEXT,
  gross_time TEXT,
  status TEXT,
  remark TEXT
);
"""
POPULATE_TABLE = f"INSERT INTO {TABLE_NAME}(place,start_no,first_name,last_name,club,country,net_time,gross_time,status,remark) VALUES(?,?,?,?,?,?,?,?,?,?)"
GET_TABLE = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute(GET_TABLE, (TABLE_NAME,))

TABLE = cur.fetchall()

if TABLE:
    print(f"{TABLE_NAME} already exists.")
    con.close()
    exit()

res = requests.get(URL)

soup = BeautifulSoup(res.text, 'html.parser')

rows = [[td.text.strip() for td in rows.select('td')]
        for rows in soup.select('tr')[1:]]


cur.execute(CREATE_TABLE)
print('Initialized the database.')
for row in rows:
    cur.execute(POPULATE_TABLE, (row[0], row[1], row[2],
                row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    con.commit()
    print('Populated the database.')

con.close()
