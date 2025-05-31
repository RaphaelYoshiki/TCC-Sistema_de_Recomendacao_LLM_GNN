import pickle
from pathlib import Path
from collections import defaultdict

def filter_and_save_pickle(input_path, output_dir="filtered_games"):
    """Filters games by review score and saves them as separate pickle files."""
    
    # Accepted review scores
    ACCEPTED_SCORES = {
        "Overwhelmingly Positive",
        "Very Positive",
        "Positive",
        "Mostly Positive",
        "Mixed"
    }
    
    # Setup output
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Track results
    results = defaultdict(dict)
    game_counts = defaultdict(int)
    
    print(f"Processing {input_path}...")
    
    try:
        with open(input_path, 'rb') as f:
            data = pickle.load(f)  # Load all data (if RAM permits)
            
            for appid, game_data in data.items():
                review_desc = game_data.get('review_score', 'no_reviews')
                apptype = game_data.get('type')
                
                if (review_desc in ACCEPTED_SCORES) and (apptype == 'game'):
                    results[review_desc][appid] = game_data
                    game_counts[review_desc] += 1
    
        # Save filtered results
        for review_desc, games in results.items():
            filename = output_path / f"{review_desc.lower().replace(' ', '_')}.p"
            with open(filename, 'wb') as f:
                pickle.dump(games, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"Saved {len(games)} {review_desc} games to {filename}")
            
        print("\nFinal counts:")
        for score, count in game_counts.items():
            print(f"- {score}: {count} games")
            
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    filter_and_save_pickle("checkpoints/apps_dict-ckpt-fin.p")