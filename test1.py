import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:
- Created a reporsitory for this project on GitHub
- Need to work on Query2 (line 18):
    figure out how to pull specific information from monday.com
- Need to confirgure the information being entered on PostgreSQL (line 45)
    data is being inserted to the table on that line, make sure the right info is going in.

'''

# Function to fetch data from Monday.com's API
def fetch_data_from_monday(api_key):
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }
    query2 = 'query { boards (limit:1) {id name} }'             # Query being passed to Monday.com to request data
    data = {'query' : query2}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from Monday.com API. Status code:", response.status_code)
        return None

# Function to insert data into PostgreSQL database
def insert_data_into_postgresql(data):
    connection = None               # initialize connection variable
    try:
        connection = psycopg2.connect(
            dbname='MeritDatabase',
            user='root',
            password='MeritControls',
            host='127.0.0.1',
            port='3306'
        )
        cursor = connection.cursor()
        
        # Insert data into a 'projects' table
        for item in data:
            # Extract specific values from item and assign them to variables
            project_name = item.get('project_name')  
            project_name_full = item.get('project_name_full')  
            customer_name = item.get('customer_name')  
            notes = item.get('notes')  
            
            # Execute the SQL INSERT statement with the extracted values
            cursor.execute("INSERT INTO projects (project_name, project_name_full, customer_name, notes) VALUES (%s, %s, %s, %s)", (project_name, project_name_full, customer_name, notes))
        
        connection.commit()
        print("Data inserted into PostgreSQL database successfully.")
        
    except (Exception, psycopg2.Error) as error:
        print("Error while inserting data into PostgreSQL database:", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed.")
        else: 
            print("No connection available.")

# Function to send data to another destination (Another API, engineers team...)
def send_data_to_another_destination(data):
    # Placeholder function for sending data to another destination
    pass

# Main function
def main():
    # Your Monday.com API key
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMxNTI1MjYyNiwiYWFpIjoxMSwidWlkIjo0NDc2ODk2MiwiaWFkIjoiMjAyNC0wMS0yOVQxNTo0NDoyMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTY4Mzg5MCwicmduIjoidXNlMSJ9.-jN2Xic1xNY9kVlr8XRYFTfy2gOLaVu9Gwp5LLfTCLk'

    # Retrieve data from Monday.com's API
    monday_data = fetch_data_from_monday(api_key)
    
    if monday_data:
        # Insert data into PostgreSQL database
        insert_data_into_postgresql(monday_data)
        
        # Send data to another destination (if needed)
        send_data_to_another_destination(monday_data)

# Entry point of the script
if __name__ == "__main__":
    main()
