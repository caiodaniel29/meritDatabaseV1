import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:
- This program prints out all the folders located in a specific workspace that is hard-coded in the query.
    It will also print all the boards located in that folder. 

- Next Goal: add this code to the main file "monday_integration" so we can print out the basic information of all the
    projects located in the Project Management workspace, and start filtering it.

'''

# Function to fetch data from Monday.com's API
def fetch_data_from_monday(api_key):
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }
    
    # Query in GraphQL to request data for all boards within the workspace
    query = 'query {\
                folders (workspace_ids: 896741) {\
                    name\
                    id\
                    children {\
                         id\
                        name\
                     }\
                }\
            }\
        '        
    data = {'query' : query}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from Monday.com API. Status code:", response.status_code)
        return None

# Function to print out data from Monday.com
def print_out_data_from_monday(data):
    folders = data.get('data', {}).get('folders', [])
    
    for folder in folders:
        folder_name = folder.get('name')
        folder_id = folder.get('id')
        print(f"\nFolder Name: {folder_name}  ||  Folder ID: {folder_id}")
        print("Projects:")
        children = folder.get('children', [])
        for child in children:
            child_id = child.get('id')
            child_name = child.get('name')
            print(f"\t{child_name}   ID: {child_id}")
        print("=" * 70)
    
    print("\nData pulled from Monday.com successfully.\n")

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

