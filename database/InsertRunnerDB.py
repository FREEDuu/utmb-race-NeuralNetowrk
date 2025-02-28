def partition_and_iterate(data, block_size=150):
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        yield block

if __name__ == "__main__":
    
    from DBconnection import ConnectionDB
    from queries.queries import FETCH_RACES_LOW_RUNNER, UPDATE_RUNNERS_RACE
    from api.utmbAPI import Scraper

    connection = ConnectionDB()
    scraper = Scraper(connection)

    races = connection.make_query(FETCH_RACES_LOW_RUNNER)

    for race in races:
        race_url, race_id = race[2], race[1]
        print('TEST -> race ', race_url, race_id)
        runners = scraper.scrape_runners_race(race_url, race_id)
        data = scraper.process_block_threaded(runners, scraper.fetch_runner)
        connection.make_insertion(UPDATE_RUNNERS_RACE, data)





