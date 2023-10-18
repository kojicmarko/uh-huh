import sys
import requests
from bs4 import BeautifulSoup
from helpers import get_table_name, is_url
import sqlite3

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

url = sys.argv[1]
table_name = get_table_name(url)
create_table = f"""
CREATE TABLE {table_name} (
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
populate_table = f"INSERT INTO {table_name}(place,start_no,first_name,last_name,club,country,net_time,gross_time,status,remark) VALUES(?,?,?,?,?,?,?,?,?,?)"
get_table = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"

con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute(get_table, (table_name,))

table = cur.fetchall()

if table:
    print(f"{table_name} already exists.")
    con.close()
    exit()

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

rows = [[td.text.strip() for td in rows.select('td')]
        for rows in soup.select('tr')[1:]]


cur.execute(create_table)
print('Initialized the database.')
for row in rows:
    cur.execute(populate_table, (row[0], row[1], row[2],
                row[3], row[4], row[5], row[6], row[7], row[8], row[9]))
    con.commit()
    print('Populated the database.')

con.close()
