import psycopg2
import pandas as pd
from sql_queries import *
import json

#  It seems that psycopg2 can't explain the np.int64 format. Looked up this workaround.
#  https://stackoverflow.com/a/56766135
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)


def get_log_data_df(filepath):
    """
    Returns log data as dataframe.
    :return: log data as dataframe
    """
    # The log files contain lines of json objects that are separated by tab and not comma.
    # I looked up how to turn a file like that into a list with multiple dictionaries.
    # https://stackoverflow.com/a/44450753
    data = []
    with open(filepath) as f:
        for line in f:
            data.append(json.loads(line))

    df = pd.DataFrame(data)

    return df


def get_time_data_df(df):
    """
    Returns timestamp details as dataframe.
    :return: timestamp details as dataframe
    """
    # convert timestamp column to datetime
    # I looked up how to convert milliseconds to a timestamp (in the context of working with dfs):
    # https://stackoverflow.com/a/61367745
    t = pd.to_datetime(df.ts, unit='ms')

    # insert time data records
    # Creating a dataframe with the timestamp series created above.
    # Using that as base/helper column to extract values and add new columns.
    time_df = pd.DataFrame({'startTime_timestamp': t})
    time_df['startTime'] = df['ts']
    time_df['hour'] = time_df['startTime_timestamp'].dt.hour
    time_df['hour'] = time_df['startTime_timestamp'].dt.hour
    time_df['day'] = time_df['startTime_timestamp'].dt.day
    time_df['week'] = time_df['startTime_timestamp'].dt.isocalendar().week
    time_df['month'] = time_df['startTime_timestamp'].dt.month
    time_df['year'] = time_df['startTime_timestamp'].dt.year
    time_df['weekday'] = time_df['startTime_timestamp'].dt.weekday

    # Deleting the helper column.
    del time_df['startTime_timestamp']

    return time_df


def process_time_data(df, cur):
    """
    Processes time data and loads it into time table.
    """
    time_df = get_time_data_df(df)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


def process_user_data(df, cur):
    """
    Processes user data and loads it into user table.
    """
    # load user table
    user_df = pd.DataFrame({'userId': df['userId'],
                            'firstName': df['firstName'],
                            'lastName': df['lastName'],
                            'gender': df['gender'],
                            'level': df['level']})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


def process_songplay_data(df, cur):
    """
    Processes songplay data and loads it into songplay table.
    """
    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results

            # As mentioned in the project specs https://review.udacity.com/#!/rubrics/2500/view,
            # there's only one match: ('SOZCTXZ12AB0182364', 'AR5KOSW1187FB35FF4')
            # print(results)

            # insert songplay record
            songplay_data = [row['ts'], row['userId'], row['level'], songid, artistid, row['sessionId']]
            cur.execute(songplay_table_insert, songplay_data)


def process_artist_data(df, cur):
    """
    Processes artist data and loads it into artist table.
    """
    # insert artist record
    artist_id = df.iloc[0]['artist_id']
    name = df.iloc[0]['artist_name']
    location = df.iloc[0]['artist_location']
    latitude = df.iloc[0]['artist_latitude']
    longitude = df.iloc[0]['artist_longitude']
    artist_data = [artist_id, name, location, latitude, longitude]
    cur.execute(artist_table_insert, artist_data)


def process_song_data(df, cur):
    """
    Processes song data and loads it into song table.
    """
    # insert song record
    song_id = df.iloc[0]['song_id']
    title = df.iloc[0]['title']
    artist_id = df.iloc[0]['artist_id']
    year = df.iloc[0]['year']
    duration = df.iloc[0]['duration']
    song_data = [song_id, title, artist_id, year, duration]
    cur.execute(song_table_insert, song_data)
