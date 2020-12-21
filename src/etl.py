import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
      Retrieve the song file, in JSON format, and 
      a. insert song data for the first record into the postgres songs table (dimension table)
      b. insert artist data for the first record into the postgres artists table (dimension table)
    Args:
         cur: Psycopg2 - a PostgreSQL database adapter for Python related to the cursor
         filepath - path of the song file
    Return : nothing
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_longitude', 'artist_latitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
      a. Retrieve the first log file, in JSON format, and 
      b. insert log data for the first record into the postgres time table (dimension table)
      c. insert artist data for the first record into the postgres users table (dimension table)
    Args:
         cur: Psycopg2 - a PostgreSQL database adapter for Python related to the cursor
         filepath - path of the song file
    Return : nothing
    """  
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == 'NextSong']

    # replace empty values with NaN
    df.replace('', float("NaN"), inplace=True)

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [(dt.timestamp(), dt.hour, dt.day, dt.week, dt.month, dt.year, dt.day_name()) for dt in t]
    column_labels = ('timestamp', 'hour', 'day', 'week of year', 'month', 'year', 'weekday')
    time_df = pd.DataFrame(time_data, columns=column_labels)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df.sort_values(by='ts', ascending=True)[['userId', 'firstName', 'lastName', 'gender', 'level']].drop_duplicates('userId').dropna(subset = ['userId'])

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)
    
    # replace timestamp to datetime
    df['ts'] = pd.to_datetime(df['ts'], unit='ms')

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (row.ts.timestamp(), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    
    """
    process data from filepath
    Args: 
        cur : psycopg2 link to cursor for postgres database
        conn : psycopg2 connection to postgres database
        filepath : path for the song data and path for the log data
        func : function name i.e. process_song_file or process_log_file
    Return : Nothing
    """
    
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
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
    """
    Script starts here
    Args : None
    Returns : None
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()