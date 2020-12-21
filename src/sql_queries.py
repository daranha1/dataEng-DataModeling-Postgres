# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
"""
  1. Create the Fact Table songplays
  2. Create the dimension Tables
     2a. users
     2b. songs
     2c. artist
     2d. time
"""
songplay_table_create = ("""
   CREATE TABLE IF NOT EXISTS songplays( \
       songplay_id SERIAL PRIMARY KEY, \
       start_time TIMESTAMP, \
       user_id int, \
       level varchar, \
       song_id varchar, \
       artist_id varchar, \
       session_id int, \
       location varchar, \
       user_agent varchar)
""")

user_table_create = ("""
  CREATE TABLE IF NOT EXISTS users( \
       user_id int PRIMARY KEY, \
       first_name varchar NOT NULL, \
       last_name varchar NOT NULL, \
       gender varchar NULL, \
       level varchar  NULL)
""")

song_table_create = ("""
  CREATE TABLE IF NOT EXISTS songs( \
       song_id varchar PRIMARY KEY, \
       title varchar NULL, \
       artist_id varchar NULL, \
       year int NULL, \
       duration decimal NULL)
""")

artist_table_create = ("""
  CREATE TABLE IF NOT EXISTS artists (\
       artist_id varchar PRIMARY KEY, \
       name varchar NULL, \
       location varchar NULL, \
       latitude float NULL, \
       longitude float NULL)
""")

time_table_create = ("""
  CREATE TABLE IF NOT EXISTS time (\
       start_time timestamp primary key, \
       hour int NOT NULL, \
       day int NOT NULL,  \
       week int NOT NULL, \
       month int NOT NULL, \
       year int NOT NULL, \
       weekday varchar NOT NULL) 
""")

# INSERT RECORDS
"""
  1. Insert records into Fact table songplays
  2. Insert records into dimension tables:
     2a. users
     2b. songs
     3c. artists
     3d. time
"""
songplay_table_insert = ("""
   INSERT INTO songplays (\
        start_time, \
        user_id, \
        level, \
        song_id, \
        artist_id, \
        session_id, \
        location, \
        user_agent) \
   VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
   INSERT INTO users (\
        user_id, \
        first_name, \
        last_name, \
        gender, \
        level) \
   VALUES (%s, %s, %s, %s, %s) \
   ON CONFLICT (user_id) DO UPDATE \
   set LEVEL = EXCLUDED.LEVEL   
""")

song_table_insert = ("""
   INSERT INTO songs (\
       song_id, \
       title, \
       artist_id, \
       year, \
       duration) \
   VALUES (%s, %s, %s, %s, %s) \
   ON CONFLICT (song_id) DO NOTHING
""")

artist_table_insert = ("""
   INSERT INTO artists (\
       artist_id, \
       name, \
       location, \
       latitude, \
       longitude) \
   VALUES (%s, %s, %s, %s, %s) \
   ON CONFLICT (artist_id) DO NOTHING
""")


time_table_insert = ("""
   INSERT INTO time (\
       start_time, \
       hour, \
       day, \
       week, \
       month, \
       year, \
       weekday) \
   VALUES (to_timestamp(%s), %s, %s, %s, %s, %s, %s) \
   ON CONFLICT (start_time) DO NOTHING
""")

# FIND SONGS

song_select = ("""
    SELECT s.song_id, a.artist_id
    FROM songs s
    INNER JOIN artists a ON s.artist_id = a.artist_id
    WHERE s.title = %s
    AND a.name = %s
    AND s.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]