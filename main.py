import sys
import requests
from bs4 import BeautifulSoup
from uhhuh.functions import get_table_name, is_url, get_sec, get_time_str, is_time
import sqlite3
import numpy as np

# 8. Krusevacki Generali polumaraton 5K M:
# res = requests.get('https://trka.rs/results/837/gender/M/')

# 2. Ulicna Trka Ecka 5K M:
# res = requests.get('https://trka.rs/results/696/gender/M/')

usr_time = sys.argv[1]
url = sys.argv[2]

if not is_time(usr_time):
    print("Invalid time format, please use H:MM:SS")
    exit()

if not is_url(url):
    print("Invalid url")
    exit()

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
read_table = f"SELECT gross_time FROM {table_name} WHERE status IS 'OK'"

con = sqlite3.connect('test.db')
cur = con.cursor()
cur.execute(get_table, (table_name,))

table = cur.fetchall()

if table:
    print(f"Retrieving data from {table_name}.")
    cur.execute(read_table)
    gross_time = [get_sec(time[0]) for time in cur.fetchall()]
    con.close()
else:
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

    cur.execute(read_table)
    gross_time = [get_sec(time[0]) for time in cur.fetchall()]
    con.close()

time_deciles = list(np.percentile(gross_time, np.arange(0, 100, 10)))

tbt = [time for time in gross_time if time < get_sec(usr_time)]

user_percentile = len(tbt) / len(gross_time) * 100

print('----------')
print(f'Faster than {100 - user_percentile:.2f}% of runners')
print('----------')
print("Average time: ", get_time_str(np.mean(gross_time)))
print('----------')
print("Median time: ", get_time_str(np.median(gross_time)))
print('----------')

i = 0
for time in time_deciles:
    if time is time_deciles[0]:
        print(f'First place: {get_time_str(time)}')
        print('----------')
    else:
        print(
            f'Top {i}% {get_time_str(time)}')
    i += 10

print('----------')
