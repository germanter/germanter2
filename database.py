import pymysql
# from dotenv import load_dotenv  ### shut down all dotenv in push
import os

# load_dotenv()  ### shut down all dotenv in push

def get_db_connection():
    return pymysql.connect(
        charset="utf8mb4",
        connect_timeout=10,
        cursorclass=pymysql.cursors.DictCursor,
        db="defaultdb",
        host="mysql-2b98ccbd-usersuer32-ae57.e.aivencloud.com",
        password=os.getenv('passdb'),  ### security
        read_timeout=10,
        port=10406,
        user="avnadmin",
        write_timeout=10,
    )

def load_data():
    connection = get_db_connection()
    try:
        dataset = []
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM market_items")
        info = cursor.fetchall()
        for i in info:
            dataset.append(dict(i))
        print("SUCCESSFUL DATABASE CONNECTION!")
        print(dataset)
    except Exception as e:
        print(f"FAILED DATABASE CONNECTION: {e}")
    finally:
        connection.close()