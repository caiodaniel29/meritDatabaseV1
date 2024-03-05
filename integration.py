import requests
import psycopg2
import json

# Author: Caio M. Sanchez
# 02/19/2024

''' 
Notes:

- Currently working on the addition of the two file folders_and_boards and monday_integration
    I have to make sure that the board`s id are being pulled goes into monday_integration function
    and prints out the information of each board. What data structure to use?        

'''


# Function to fetch the board`s name and ID from Monday.com's API
def fetch_boardsID_from_monday(api_key):
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

# Function to organize the boards data from monday.com
def organize_boardsID_from_monday(data):
    folders = data.get('data', {}).get('folders', [])
    boards_IDs = []
    
    for folder in folders:
        children = folder.get('children', [])
        for child in children:
            child_id = child.get('id')
            boards_IDs.append(child_id)
    
    # print(boards_IDs)
    print("\nData pulled from Monday.com successfully.\n")
    return boards_IDs

# Function to use the board data to get more information on each board.
def fetch_data_from_monday(api_key, boards_IDs):
    apiUrl = 'https://api.monday.com/v2/'
    headers = {'Authorization': api_key }

    for board_id in boards_IDs:
        # Query in GraphQL being passed to Monday.com to request data
        query = f'''
            query {{
                boards (ids: [{board_id}]) {{
                    id
                    name
                    description
                }}
            }}
        '''
        data = {'query': query}

        response = requests.post(url=apiUrl, json=data, headers=headers)

        if response.status_code == 200:
            board_data = response.json()
            print_out_data_from_monday(board_data)
        else:
            print(f"Failed to retrieve data for board ID {board_id} from Monday.com. Status code:", response.status_code)

# Function to print out the data for a specific board
def print_out_data_from_monday(data):
    boards = data.get('data', {}).get('boards', [])

    for board in boards:
        board_id = board.get('id')
        board_name = board.get('name')
        abbreviation = board_name[:4]
        full_name = board_name[7:]
        board_description = board.get('description')

        # Slicing the Customer name from board description
        start_phrase = "Owner: "
        end_phrase = "Customer: "
        start_index = board_description.find(start_phrase)
        end_index = board_description.find(end_phrase)
        owner_name = board_description[start_index + len(start_phrase):end_index].strip()

        # Printing the information pulled from Monday.com
        print(f"\nBoard: {abbreviation}\nBoard Name: {full_name}\nBoard ID: {board_id}\nOwner Name: {owner_name}\n")

# Function to print out the data that would go into PostgreSQL database
def print_out_dataq_from_monday(data):
      '''  
    boards = data.get('data', {}).get('boards', [])
    for board in boards:
        board_id = board.get('id')
        board_name = board.get('name')
        abbreviation = board_name[:4]
        full_name = board_name[7:]
        board_description = board.get('description')

        # Slicing the Customer name from board description
        start_phrase = "Owner: "
        end_phrase = "Customer: "
        start_index = board_description.find(start_phrase)
        end_index = board_description.find(end_phrase)
        owner_name = board_description[start_index + len(start_phrase):end_index].strip()

        # Printing the information pulled from Monday.com
        print(f"\nBoard: {abbreviation}\nBoard Name: {full_name}\nBoard ID: {board_id}\nOwner Name: {owner_name}\n")

        
        columns = board.get('columns', [])
        for column in columns:
            column_id = column.get('id')
            column_title = column.get('title')
            column_type = column.get('type')
            print(f"\tColumn ID: {column_id}, Title: {column_title}, Type: {column_type}")
        

        print("\nData pulled from Monday.com successfully.\n")
        '''
        
    

# Main function
def main():
    # Your Monday.com API key
    api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjMxNTI1MjYyNiwiYWFpIjoxMSwidWlkIjo0NDc2ODk2MiwiaWFkIjoiMjAyNC0wMS0yOVQxNTo0NDoyMS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6OTY4Mzg5MCwicmduIjoidXNlMSJ9.-jN2Xic1xNY9kVlr8XRYFTfy2gOLaVu9Gwp5LLfTCLk'

    # Retrieve the boards` ID from Monday.com's API
    monday_data = fetch_boardsID_from_monday(api_key)

    if monday_data:
        # Organize the board`s ID data from monday.com
        boards_IDs = organize_boardsID_from_monday(monday_data)

        # Pull boards information with the IDs and print out
        data = fetch_data_from_monday(api_key, boards_IDs)

        print_out_data_from_monday(data)

# Entry point of the script
if __name__ == "__main__":
    main()
