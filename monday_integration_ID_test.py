import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:
- Currently working on the addition of all the boards to my program
    trying the PM Workspace ID right now

- Trying to make the program run with the workspace id

'''


    # Function to fetch data from Monday.com's API
def fetch_data_from_monday(api_key, workspace_id):
    global workspace_id  # Declare workspace_id as globalglobal workspace_id  # Declare workspace_id as global
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }
    
    # Query in GraphQL to request data for all boards within the workspace
    query = f'query {{ \
        boards (workspace_id: {workspace_id}) {{ \
              id \
              name \
              description \
              columns {{ \
                 id \
                 title \
                 type \
                }} \
            }}\
    }}'        
    data = {'query' : query}

    response = requests.post(url=apiUrl, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve data from Monday.com API. Status code:", response.status_code)
        return None

# Function to print out data from Monday.com
def print_out_data_from_monday(data):
    boards = data.get('data', {}).get('boards', [])
    for board in boards:
        board_id = board.get('id')
        board_name = board.get('name')
        board_description = board.get('description', '')
        
        # Print board information
        print(f"Board ID: {board_id}")
        print(f"Board Name: {board_name}")
        print(f"Board Description: {board_description}")
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
    workspace_id = '896741'

    main()
