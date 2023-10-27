from os import walk
import cyrtranslit
import csv
import sqlite3

con = sqlite3.connect('trka.db')
cur = con.cursor()

w = walk('event_results/')

event_paths = []
for dirpath, dirnames, filenames in w:
    event_paths.append(dirpath)

for i, event_path in enumerate(event_paths[1:]):
    with open(f'{event_path}/races') as f:
        lines_from_races_file = [line.strip() for line in f]
    race_name = cyrtranslit.to_latin(lines_from_races_file.pop(0))
    races = []
    print(i, event_path)
    for race in lines_from_races_file:
        distance = race.split(']')[0].replace('[', '').replace(' ', '')
        race = f"{race.split(']')[1].strip()}.csv"
        races.append((race, distance))

    for race in races:
        with open(f'{event_path}/{race[0]}') as csvfile:
            reader = csv.DictReader(csvfile)
            distance = race[1]
            race_id = event_path[15:18]
            for row in reader:
                if row['status'] == 'OK':
                    row['race_name'] = race_name
                    row['race_id'] = race_id
                    row['distance'] = distance
                    if row['gender'] == 'Мушки':
                        row['gender'] = 'M'
                    elif row['gender'] == 'Женски':
                        row['gender'] = 'F'
                    row_lst = list(row.values())
                    cur.execute("INSERT INTO races(rank,number,first_name,last_name,gender,birth_year,club,city,country,chip_time,gun_time,status,race_name,race_id,distance) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", row_lst)

con.commit()
con.close()
