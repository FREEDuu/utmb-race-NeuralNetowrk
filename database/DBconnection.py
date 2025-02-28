from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import psycopg2
import psycopg2.extras

load_dotenv()

# Parse database URL
database_url = os.getenv("DATABASE_URL")
tmpPostgres = urlparse(database_url)
db_name = tmpPostgres.path[1:]  

DATABASES = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': db_name,
    'USER': tmpPostgres.username,
    'PASSWORD': tmpPostgres.password,
    'HOST': tmpPostgres.hostname,
    'PORT': 5432,
}

class ConnectionDB:
    def __init__(self):
        self.DB = DATABASES
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.DB['NAME'], user=self.DB['USER'], password=self.DB['PASSWORD'], host=self.DB['HOST'], port=self.DB['PORT']
            )
            self.connection = conn
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            return None

    def make_query(self, query):
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
        

    def make_insertion(self, query, data):

        cleaned_data = [item for item in data if all(value is not None for value in item)]
        print(f"""
            runner nuovi {len(cleaned_data)} runner totali {len(data)}
            runner aggiunti {cleaned_data}

        """)
        psycopg2.extras.execute_batch(self.cursor, query, cleaned_data)
        self.connection.commit()

        return 'Insertion Success'
    
    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Connection closed.") #for debugging
