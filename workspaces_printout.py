import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:
- In this file I was able to pull the information of the workspaces located in my Monday.com account, with some information.

- Goal: to get more information on only one workspace

'''

# Define workspace_id as a global variable
global workspace_id

# Function to fetch data from Monday.com's API
def fetch_data_from_monday(api_key):
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }
    global workspace_id
    
    # Query in GraphQL to request data for all boards within the workspace
    query = '''query { \
               workspaces  { \
                 id \
                 name \
                 kind \
                 state \
               }\
    }'''        
    data = {'query' : query}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from Monday.com API. Status code:", response.status_code)
        return None

# Function to print out data from Monday.com
def print_out_data_from_monday(data):
    workspaces = data.get('data', {}).get('workspaces', [])
    for workspace in workspaces:
        workspace_id = workspace.get('id')
        workspace_name = workspace.get('name')
        workspace_kind = workspace.get('kind')
        workspace_state = workspace.get('state')

        # Print board information
        print(f"\nWorkspace ID: {workspace_id}")
        print(f"Workspace Name: {workspace_name}")
        print(f"Workspace Kind: {workspace_kind}")
        print(f"Workspace State: {workspace_state}")
        print("="*30)
    
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

    # My workspace ID 
    workspace_id = '4638100743'

    main()
