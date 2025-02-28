def partition_and_iterate(data, block_size=150):
    for i in range(0, len(data), block_size):
        block = data[i:i + block_size]
        yield block

if __name__ == "__main__":
    
    from DBconnection import ConnectionDB
    from queries.queries import FETCH_ALL_RACES, UPDATE_RACE
    from api.utmbAPI import Scraper

    connection = ConnectionDB()
    scraper = Scraper(connection)

    result = connection.make_query(FETCH_ALL_RACES)

    for block in partition_and_iterate(result):

        data = scraper.process_block_threaded(block, scraper.scrape_race_data)
        print('DATA', data)
        connection.make_insertion(UPDATE_RACE, data)


