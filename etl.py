import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
import json

#  It seems that psycopg2 can't explain the np.int64 format. Looked up this workaround.
#  https://stackoverflow.com/a/56766135
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


def process_song_file(cur, filepath):
    # open song file
    with open(filepath, 'r') as f:
        # String needs to be transformed first into a dictionary.
        data = json.load(f)

    df = pd.DataFrame(data, index=['song_id'])

    # insert artist record
    artist_id = df.iloc[0]['artist_id']
    name = df.iloc[0]['title']
    location = df.iloc[0]['artist_location']
    latitude = df.iloc[0]['artist_latitude']
    longitude = df.iloc[0]['artist_longitude']
    artist_data = [artist_id, name, location, latitude, longitude]
    cur.execute(artist_table_insert, artist_data)

    # insert song record
    song_id = df.iloc[0]['song_id']
    title = df.iloc[0]['title']
    artist_id = df.iloc[0]['artist_id']
    year = df.iloc[0]['year']
    duration = df.iloc[0]['duration']
    song_data = [song_id, title, artist_id, year, duration]
    cur.execute(song_table_insert, song_data)


def process_log_file(cur, filepath):
    # open log file

    # The log files contain lines of json objects that are separated by tab and not comma.
    # I looked up how to turn a file like that into a list with multiple dictionaries.
    # https://stackoverflow.com/a/44450753
    data = []
    with open(filepath) as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.DataFrame(data)

    # filter by NextSong action
    # Create a filter.
    filterNextSong = df['page'] == 'NextSong'

    # Apply the filter and remove rows that contain nulls.
    df = df.where(filterNextSong).dropna()

    # convert timestamp column to datetime
    # I looked up how to convert milliseconds to a timestamp (in the context of working with dfs):
    # https://stackoverflow.com/a/61367745
    t = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    # Creating a dataframe with the timestamp series created above.
    # Using that as base to extract values and add new columns.
    time_df = pd.DataFrame({'startTime': t})
    time_df['hour'] = time_df['startTime'].dt.hour
    time_df['hour'] = time_df['startTime'].dt.hour
    time_df['day'] = time_df['startTime'].dt.day
    time_df['week'] = time_df['startTime'].dt.isocalendar().week
    time_df['month'] = time_df['startTime'].dt.month
    time_df['year'] = time_df['startTime'].dt.year
    time_df['weekday'] = time_df['startTime'].dt.weekday

    # for i, row in time_df.iterrows():
    #     cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame({'userId': df['userId'],
                            'firstName': df['firstName'],
                            'lastName': df['lastName'],
                            'gender': df['gender'],
                            'level': df['level']})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    #
    # # insert songplay records
    # for index, row in df.iterrows():
    #
    #     # get songid and artistid from song and artist tables
    #     cur.execute(song_select, (row.song, row.artist, row.length))
    #     results = cur.fetchone()
    #
    #     if results:
    #         songid, artistid = results
    #     else:
    #         songid, artistid = None, None
    #
    #     # insert songplay record
    #     songplay_data = ""
    #     cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, '*.json'))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    # process_data(cur=cur, conn=conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
