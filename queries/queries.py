# QUERY THAT FETCH ALL RACE WITHOUT TITLE ECC . . .

FETCH_ALL_RACES = """
    select * from races_table where races_table.race_title is null order by race_id DESC
"""

# QUERY THAT FETCH ALL RACE WITh low amount of runner associated . . .

FETCH_RACES_LOW_RUNNER = """
select count(*), rr.race_id, rt.race_url from races_table rt, runner_race rr
where rr.race_id = rt.race_id group by rr.race_id, rt.race_url order by count(*) ASC
"""

# QUERY THAT UPDATE A RACE THAT DOESNT HAVE NAME , TITLE ECC.

UPDATE_RACE = """
UPDATE races_table SET race_title = %s, race_elevation = %s, race_distance = %s WHERE race_id = %s
"""

UPDATE_RUNNERS_RACE = """
INSERT INTO runner_race (race_id, runner_url, runner_name, runner_finish_time, runner_utmb_index) VALUES (%s, %s, %s, %s, %s)
"""