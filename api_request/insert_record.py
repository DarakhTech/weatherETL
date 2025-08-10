from api_requests import fetch_data, mock_fetch_data
import psycopg2
import csv

def connect_to_db():
    print("Connecting to the database...")
    
    try:
        conn = psycopg2.connect(
            dbname='db',
            user='user',
            password='password',
            host='localhost',
            port='8000'
            # host='db',
            # port='5432'
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def create_table(conn):
    print("Creating table if it doesn't exist...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature INT,
                weather_description TEXT,
                wind_speed INT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
        """)
        conn.commit()
        print("Table created successfully.")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()
        raise

def get_analytics(conn):
    print("Fetching analytics...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM dev.daily_average;
        """)
        data = cursor.fetchall()
        conn.commit()
        # print(data)
        return data
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()
        raise
    
# conn = connect_to_db()
# create_table(conn)

def insert_record(conn, data):
    print("Inserting record into the database...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
           INSERT INTO dev.weather_data (city, temperature, weather_description, wind_speed, time, inserted_at, utc_offset)
           VALUES (%s, %s, %s, %s, %s, NOW(), %s)
                       
        """,(
            data['location']['name'],
            data['current']['temperature'],
            ', '.join(data['current']['weather_descriptions']),
            data['current']['wind_speed'],
            data['location']['localtime'],
            data['location']['utc_offset']
        ))
        conn.commit()
        print("Record inserted successfully.")
    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")
        conn.rollback()
        raise
    
# print(mock_fetch_data()['current']['weather_descriptions'])

def main():
    try:
        conn = connect_to_db()
        create_table(conn)
        # data = mock_fetch_data()  # Use mock data for testing
        data = fetch_data()  # Use mock data for testing

        insert_record(conn, data)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

def export_csv():
    try:
        conn = connect_to_db()
        # data = mock_fetch_data()  # Use mock data for testing
        data = get_analytics(conn)  # Use mock data for testing
        
        if data is not None or len(data) != 0:    
            headers = ["city", "date", "avg_temperature", "avg_wind_speed"]
            with open("../reports/daily_average.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)  
                for row in data:
                    writer.writerow(row)   
            print("Data exported successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

# main()
export_csv()