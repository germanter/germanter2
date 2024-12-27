import pymysql
# from dotenv import load_dotenv  ### shut down all dotenv in push

# import os

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
        return dataset
    except Exception as e:
        print(f"FAILED DATABASE CONNECTION: {e}")
    finally:
        connection.close()

def load_item(id):
    connection = get_db_connection()
    try:
        dataset = []
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM market_items WHERE id = %s", (id,))
        info = cursor.fetchall()
        for i in info:
            dataset.append(dict(i))
        print("SUCCESSFUL DATABASE CONNECTION!")
        return dataset
    except Exception as e:
        print(f"FAILED DATABASE CONNECTION: {e}")
    finally:
        connection.close()
        
def insert_application(user_data):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES(%s, %s, %s)",
            (
                user_data[0],
                user_data[1],
                user_data[2],
            ),
        )
        connection.commit()
        print("USER SUCCESSFULLY INSERTED!")
    except Exception as e:
        print(f"FAILED TO INSERT USER: {e}")
        return list(e.args)
    finally:
        connection.close()
        
def get_user_with_email(email):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email,password FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()  # Fetch one record
        
        if result:
    
            return result
        else:
            return None  # No user found
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        connection.close()
        
def get_user_with_id(user_id):
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, email,password FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()  # Fetch one record
        
        if result:
            
            return result
        else:
            return None  # No user found
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        connection.close()
        
        
        
        