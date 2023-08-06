import psycopg2
from psycopg2 import Error
from dotenv import load_dotenv
import os
import json


def import_data_to_db():
    load_dotenv()
    user = os.getenv("db_user")
    password = os.getenv("db_password")
    host = os.getenv("db_host")
    port = os.getenv("db_port")
    database = os.getenv("db_database")

    try:
        # Connect to an existing database
        connection = psycopg2.connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)

        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")
        # Open the output.json file
        with open('data/output_FI_DayAheadPrices.json', 'r') as fp:
            priceRows = json.load(fp)
            for row in priceRows:
                # Extract the values from the row dictionary
                datetime = row['datetime']
                pricewithouttax = row['pricewithouttax']
                pricewithtax = row['pricewithtax']

            # SQL INSERT
                insert_prices = f"INSERT INTO fiPrices (datetime, pricewithouttax, pricewithtax) VALUES ('{datetime}', {pricewithouttax}, {pricewithtax});"

            # try INSERT data skipping duplicates (unique datetime)
                try: 
                    with connection.cursor() as cursor:
                        cursor.execute(insert_prices)
                except Error as e:
                    print(f'Error: {e}')
                    connection.rollback()
        connection.commit()
        print("Price data inserted successfully")

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):

            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
            # clear data folder when upload is done
            directory = './data'
            for file in os.listdir(directory):
                os.remove(os.path.join(directory, file))
