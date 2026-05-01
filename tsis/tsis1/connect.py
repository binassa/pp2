import psycopg2


def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="phonebook_db",  
            user="sabina",        
            password="", 
            port="5432"
        )
        return conn

    except Exception as e:
        print("Error connecting to database:", e)