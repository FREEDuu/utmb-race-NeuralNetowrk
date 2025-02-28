import pandas as pd
from DBconnection import ConnectionDB

if __name__ == "__main__":

    DB = ConnectionDB()
    DB.connect()
    conn = DB.connection

    # Load races data
    races_df = pd.read_sql("""
        SELECT race_id, race_title, race_distance, race_elevation 
        FROM races_table
    """, conn)

    # Load runner data
    runner_df = pd.read_sql("""
        SELECT race_id, runner_id, runner_utmb_index, runner_finish_time 
        FROM runner_race
    """, conn)

    races_df.to_csv('raceDF.csv', index=False)
    runner_df.to_csv('runnerDF.csv', index=False)