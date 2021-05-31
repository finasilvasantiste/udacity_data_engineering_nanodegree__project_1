# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
CREATE TABLE songplays (
   songplay_id SERIAL PRIMARY KEY,
   start_time NUMERIC NOT NULL,
   user_id INTEGER REFERENCES users(user_id),
   level VARCHAR(250) NOT NULL,
   song_id VARCHAR(250) REFERENCES songs(song_id),
   artist_id VARCHAR(250) REFERENCES artists(artist_id),
   session_id NUMERIC NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE users (
   user_id SERIAL PRIMARY KEY,
   first_name VARCHAR (255) NOT NULL,
   last_name VARCHAR (255) NOT NULL,
   gender VARCHAR (255) NOT NULL,
   level VARCHAR (255) NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE songs (
   song_id VARCHAR (255) PRIMARY KEY,
   title VARCHAR (255) NOT NULL,
   artist_id VARCHAR (255) references artists(artist_id),
   year NUMERIC NOT NULL,
   duration NUMERIC NOT NULL
);
""")

artist_table_create = ("""
CREATE TABLE artists (
   artist_id VARCHAR (255) PRIMARY KEY,
   name VARCHAR (255) NOT NULL,
   location VARCHAR (255),
   latitude NUMERIC (255),
   longitude NUMERIC (255)
);
""")

time_table_create = ("""
CREATE TABLE time (
   start_time NUMERIC PRIMARY KEY,
   hour VARCHAR (255) NOT NULL,
   day VARCHAR (255) NOT NULL,
   week NUMERIC (255) NOT NULL,
   month NUMERIC (255) NOT NULL,
   year NUMERIC (255) NOT NULL,
   weekday NUMERIC (255) NOT NULL
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s);
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s);
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [artist_table_create, user_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
