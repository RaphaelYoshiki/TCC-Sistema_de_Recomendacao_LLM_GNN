import pickle
import json
import os

def pickle_to_json(pickle_filepath, json_filepath=None):
    """
    Converts a pickle file to a JSON file.
    
    Args:
        pickle_filepath (str): The path to the input pickle file.
        json_filepath (str, optional): The path to the output JSON file. 
            If None, it defaults to the pickle filename with a .json extension.
    """
    if json_filepath is None:
      # Replace the extension with .json
      json_filepath = os.path.splitext(pickle_filepath)[0] + '.json'
    
    try:
        with open(pickle_filepath, 'rb') as file:
            data = pickle.load(file)
    except FileNotFoundError:
        print(f"Error: Pickle file not found at '{pickle_filepath}'")
        return
    except Exception as e:
         print(f"An error occurred while reading the pickle file: {e}")
         return

    try:
        with open(json_filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully converted '{pickle_filepath}' to '{json_filepath}'")
    except Exception as e:
        print(f"An error occurred while writing the JSON file: {e}")
        return

# Example usage:
pickle_file = 'filtered_games/overwhelmingly_positive.p'
json_file = 'utilitary_codes/steam_gamedata.json' 
pickle_to_json(pickle_file, json_file) # You can omit json_file to generate it automatically