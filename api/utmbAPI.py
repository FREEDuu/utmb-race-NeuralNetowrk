import requests
from bs4 import BeautifulSoup
import threading
from api.user_agent.agent import get_random_user_agent
import random, time

class Scraper:

    def __init__(self, connection_DB):
        self.url = 'https://api.utmb.world'
        self.url_result = 'https://api.utmb.world/races/'
        self.race_url_base = 'https://utmb.world/utmb-index/races/'
        self.OFFESET_RACE = 25
        self.connection_DB = connection_DB

    def process_block_threaded(self, block, target_function, delay_range=(0.01, 0.05)):
        results = []
        threads = []

        def wrapped_target(*args):
            if target_function == self.scrape_race_data:
                id, race_id = args[0], args[1]
                result = target_function(race_id) 
                results.append(result + (id,))
            if target_function == self.fetch_runner:
                result = target_function(*args) 
                results.append(result)

        for item in block:
            thread = threading.Thread(target=wrapped_target, args=item)
            threads.append(thread)
            thread.start()
            delay = random.uniform(delay_range[0], delay_range[1])
            time.sleep(delay)

        for thread in threads:
            thread.join()

            return results

    def get_url_runner(self, runner_url):
        return f'https://utmb.world/it/runner/{runner_url}'

    def get_url_race(self, race_url, counter):
        return f'{self.url_result}{race_url}/results?lang=it&offset={counter*self.OFFESET_RACE}&gender='

    def scrape_race_data(self, race):
        """
        Scrapes race title, distance, and elevation gain from a given URL.
        """
        try:

            headers = {'User-Agent': get_random_user_agent()}
            response = requests.get(self.race_url_base + race, headers=headers, timeout=15)
            response.raise_for_status()

            html = response.content
            soup = BeautifulSoup(html, 'html.parser')

            title_element = soup.find('h1', class_='race-header_rh_race_title__COtYd')
            distance_element = soup.find('p', string='Distance').find_next_sibling('span')
            elevation_element = soup.find('p', string='Elevation Gain').find_next_sibling('span')

            title = title_element.text.strip() if title_element else None
            distance = distance_element.text if distance_element else None
            elevation = elevation_element.text if elevation_element else None

            return (title, distance, elevation)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching URL: {e}")
            return (None, None, None)
        except AttributeError:
            print("Could not find required elements on the page.")
            return (None, None, None)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return (None, None, None)
        
    def fetch_runner(self, race_id, runner_url, fullname, time_race):
        try:         
            url = self.get_url_runner(runner_url)
            print('TEST URL', url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            class_name = "font-16 font-d-20 font-oxanium-bold performance_stat__hcZM_"  # class to find UTMB index number to scrape
            element = soup.find(class_=class_name)
            runner_name, runner_time, index = fullname, time_race , int(element.text)
            return (race_id, runner_url, runner_name, runner_time, index)

        except Exception as e:
            print('URL errato o runner non esistente')
            return (None, None, None)

    def scrape_runners_race(self, race_url, race_id):
        counter = 0
        all_values = []

        while True:
            req = requests.get(self.get_url_race(race_url, counter))
            try:
                results = req.json()['results']
                if not results:
                    return all_values
                for item in results:
                    all_values.append((race_id, item['runnerUri'], item['fullname'], item['time']))
                counter += 1 
            except (requests.exceptions.RequestException, KeyError, ValueError):
                return all_values
