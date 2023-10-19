-- DROP TABLE IF EXISTS race;
-- DROP TABLE IF EXISTS racer;

CREATE TABLE race (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  race_name TEXT NOT NULL UNIQUE
);

CREATE TABLE runner (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  race_name TEXT NOT NULL,
  rank INTEGER,
  number INTEGER,
  first_name TEXT,
  last_name TEXT,
  club TEXT,
  country TEXT,
  chip_time TEXT,
  gun_time TEXT,
  status TEXT,
  remark TEXT,
  FOREIGN KEY (race_name) REFERENCES race (race_name)
);