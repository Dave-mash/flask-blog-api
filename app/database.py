import psycopg2
import os

class InitializeDb:
    """ This class sets up database connection and creates tables """

    @classmethod
    def __init__(cls, db_url):
        cls.env = db_url.ENV


    @classmethod
    def init_db(cls, db_url):
        try:
            print(os.getenv('TEST_DATABASE_URI'))
            cls.connection = psycopg2.connect(db_url.DB_URL)
            cls.cursor = cls.connection.cursor()
            print(f'A connection to {db_url.DB_URL} database was established!')
            return cls.cursor
        except:
            print(db_url)
            print(f'A problem occured while connecting to the {db_url.DB_URL}')


    @classmethod
    def create_tables(cls):
        """ This method creates tables """

        cls.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id serial PRIMARY KEY NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                image VARCHAR NOT NULL,
                date_registered TIMESTAMP DEFAULT current_timestamp
            );
            CREATE TABLE IF NOT EXISTS posts(
                id serial PRIMARY KEY NOT NULL,
                author_id INT REFERENCES users(id)\
                ON UPDATE CASCADE ON DELETE CASCADE,
                title TEXT UNIQUE NOT NULL,
                body TEXT NOT NULL,
                created_on TIMESTAMP DEFAULT current_timestamp
            );
            CREATE TABLE IF NOT EXISTS comments(
                id serial PRIMARY KEY NOT NULL,
                user_id INT REFERENCES users(id)\
                ON UPDATE CASCADE ON DELETE CASCADE,
                post_id INT REFERENCES posts(id)\
                ON UPDATE CASCADE ON DELETE CASCADE,
                comment TEXT NOT NULL,
                created_on TIMESTAMP DEFAULT current_timestamp
            );
            CREATE TABLE IF NOT EXISTS blacklist(
                id serial PRIMARY KEY NOT NULL,
                username VARCHAR REFERENCES users(username)\
                ON UPDATE CASCADE ON DELETE CASCADE,
                tokens VARCHAR NOT NULL
            );
            """
        )

        cls.connection.commit()

    
    @classmethod
    def execute(cls, query):
        """ This method saves values into the db """
        print(query)
        cls.cursor.execute(query)
        cls.connection.commit()
    
    
    @classmethod
    def fetch_all(cls, query):
        """ This method fetches all items """
        
        cls.cursor.execute(query)
        return cls.cursor.fetchall()
    
    
    @classmethod
    def fetch_one(cls, query):
        """ This method fetches a single item """
        
        cls.cursor.execute(query)
        return cls.cursor.fetchone()
    
    
    @classmethod
    def update(cls, query):
        """ This method executes update queries """
        print(query)
        cls.cursor.execute(query)
        cls.connection.commit()


    @classmethod
    def drop_tables(cls):
        """ This method drops all tables """
        
        cls.cursor.execute("DROP TABLE IF EXISTS users, posts, comments CASCADE;")
        cls.connection.commit()


# TIME
# from datetime import datetime

    # normal time --> timestamp
     # time = datetime.now()
     # datetime.timestamp(time)

    # timestamp --> normal time
     # timestamp = 34103718234.89098
     # time = datetime.fromtimestamp(timestamp)
 
