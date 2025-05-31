import os
import json
import pickle
from pathlib import Path
from collections import defaultdict

def extract_unique_values():
    # Initialize storage
    unique_data = {
        'developers': set(),
        'publishers': set(),
        'categories': set(),
        'genres': set()
    }

    # Path setup
    input_dir = Path('normalized_filtered_games')
    output_dir = Path('gamedata_value_lists')
    output_dir.mkdir(exist_ok=True)

    # Process all pickle files
    for pickle_file in input_dir.glob('*.p'):
        with open(pickle_file, 'rb') as f:
            games_data = pickle.load(f)
            
            for game_id, game in games_data.items():
                # Extract developers
                if 'developers' in game:
                    unique_data['developers'].update(game['developers'])
                
                # Extract publishers
                if 'publishers' in game:
                    unique_data['publishers'].update(game['publishers'])
                
                # Extract categories
                if 'categories' in game:
                    for category in game['categories']:
                        if isinstance(category, dict) and 'description' in category:
                            unique_data['categories'].add(category['description'])
                
                # Extract genres
                if 'genres' in game:
                    for genre in game['genres']:
                        if isinstance(genre, dict) and 'description' in genre:
                            unique_data['genres'].add(genre['description'])

    # Convert sets to sorted lists and save
    for key, values in unique_data.items():
        sorted_values = sorted(list(values))
        output_file = output_dir / f'{key}_list.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sorted_values, f, indent=2, ensure_ascii=False)
        
        print(f'Saved {len(sorted_values)} {key} to {output_file}')

if __name__ == '__main__':
    extract_unique_values()