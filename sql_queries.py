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
   user_id NUMERIC REFERENCES users(user_id),
   level VARCHAR(250) NOT NULL,
   song_id VARCHAR(250) REFERENCES songs(song_id),
   artist_id VARCHAR(250) REFERENCES artists(artist_id),
   session_id NUMERIC NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE users (
   user_id NUMERIC PRIMARY KEY,
   first_name VARCHAR (255) NOT NULL,
   last_name VARCHAR (255) NOT NULL,
   gender VARCHAR (1) NOT NULL,
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
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id)
VALUES(%s, %s, %s, %s, %s, %s)
""")

# I'm assuming a row with an user_id that already exists in the table
# is a row with identical values, that's why I'm using ON CONFLICT DO NOTHING.
user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET level = EXCLUDED.level;
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")


# I'm assuming a row with an artist_id that already exists in the table
# is a row with identical values, that's why I'm using ON CONFLICT DO NOTHING.
artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")


# Since we're using the time table as a kind of look-up dictionary
# each row is unique. If we want to insert a row with a timestamp that already
# exists in the table we can safely ignore it, that's why I'm using ON CONFLICT DO NOTHING.
time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
""")

# FIND SONGS

song_select = ("""
SELECT DISTINCT s.song_id, s.artist_id
FROM songs s JOIN artists a ON s.artist_id = a.artist_id
WHERE s.title = %s
AND a.name = %s
AND s.duration = %s
;
""")

# QUERY LISTS

create_table_queries = [artist_table_create, user_table_create, song_table_create, time_table_create, songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
