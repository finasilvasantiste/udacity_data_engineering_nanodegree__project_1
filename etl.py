from etl_transform_and_load import process_song_data, process_artist_data, process_user_data,\
    process_songplay_data, process_time_data, get_log_data_df
import os
import glob
import psycopg2
import pandas as pd
import json


def process_song_file(cur, filepath):
    """
    Processes song data and loads it into song and artist tables accordingly.
    """
    # open song file
    with open(filepath, 'r') as f:
        # String needs to be transformed first into a dictionary.
        data = json.load(f)

    df = pd.DataFrame(data, index=['song_id'])

    # Process data for each table.
    process_artist_data(df=df, cur=cur)
    process_song_data(df=df, cur=cur)


def process_log_file(cur, filepath):
    """
    Processes log data and loads it into time, user and songplay tables accordingly.
    """
    # open log file
    df = get_log_data_df(filepath)

    # filter by NextSong action
    # Create a filter.
    filterNextSong = df['page'] == 'NextSong'
    # Apply the filter and remove rows that contain nulls.
    df = df.where(filterNextSong).dropna()

    # Process data for each table.
    process_time_data(df=df, cur=cur)
    process_user_data(df=df, cur=cur)
    process_songplay_data(df=df, cur=cur)


def process_data(cur, conn, filepath, func):
    """
    Processes given data using given function.
    """
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

    process_data(cur=cur, conn=conn, filepath='data/song_data', func=process_song_file)
    process_data(cur=cur, conn=conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
