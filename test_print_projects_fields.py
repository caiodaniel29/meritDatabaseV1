import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:
- Currently working on the part of pulling information from monday on this file
    goal is to be able to print out that data and manipulate it.

'''

# Function to fetch data from Monday.com's API
def fetch_data_from_monday(api_key):
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }
     # Query in GraphQL being passed to Monday.com to request data
    query2 = 'query { \
        boards (ids: [1234567890, 9876543210]) { \
              id \
              name \
              columns { \
                 id \
                 title \
                 type \
                } \
            }\
    }'        
    data = {'query' : query2}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from Monday.com API. Status code:", response.status_code)
        return None

# Function to insert data into PostgreSQL database
def print_out_data_from_monday(data):
        """
        # Insert data into a 'projects' table
        for item in data:
            # Extract specific values from item and assign them to variables to be sent to SQL
            project_name = item.get('project_name')  
            project_name_full = item.get('project_name_full')  
            customer_name = item.get('customer_name')  
            notes = item.get('notes')  
            
            # Print out the information
            print("Project name: ", project_name)
            print("Project full name: ", project_name_full)
            print("Customer name: ", customer_name)
            print("Notes: ", notes)
        """
        print(monday_data)
        print("Data pulled from Monday.com successfully.")
        
    

# Main function
def main():
    # Your Monday.com API key
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMxNTI1MjYyNiwiYWFpIjoxMSwidWlkIjo0NDc2ODk2MiwiaWFkIjoiMjAyNC0wMS0yOVQxNTo0NDoyMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTY4Mzg5MCwicmduIjoidXNlMSJ9.-jN2Xic1xNY9kVlr8XRYFTfy2gOLaVu9Gwp5LLfTCLk'

    # Retrieve data from Monday.com's API
    monday_data = fetch_data_from_monday(api_key)
    
    if monday_data:
        # Print out the data pulled from Monday.com
        print_out_data_from_monday(monday_data)

# Entry point of the script
if __name__ == "__main__":
    main()
