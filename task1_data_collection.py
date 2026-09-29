"""
TASK 1: Fetch Data from HackerNews API
This script collects trending stories and saves them as JSON  
"""

# STEP 1: Import libraries
import requests  # fetch data from internet
import time      # pause between requests
import json      # work with JSON files
import os        # create folders
from datetime import datetime  # work with dates/times


# STEP 2: Setup - Define the API links and keywords 

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
STORY_URL = "https://hacker-news.firebaseio.com/v0/item/{id}.json"

# Custom header to identify our script  
  HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Define categories and keywords
# If a story title contains these keywords, it goes into that category

CATEGORIES = {
    "technology": [
        "AI", "machine learning", "python", "software", "tech", 
        "code", "computer", "data", "cloud", "API", "GPU", "LLM",
        "programming", "algorithm", "database", "server"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election", 
        "climate", "attack", "global", "international", "politics",
        "crisis", "diplomacy", "treaty", "united nations"
    ],
    "sports": [
        "NFL", "NBA", "FIFA", "sport", "game", "team", "player", 
        "league", "championship", "match", "cricket", "tennis",
        "goal", "score", "tournament", "coach"
    ],
    "science": [
        "research", "study", "space", "physics", "biology", 
        "discovery", "NASA", "genome", "scientist", "experiment",
        "medical", "health", "quantum", "relativity", "atom"
    ],
    "entertainment": [
        "movie", "film", "music", "Netflix", "game", "book", "show", 
        "award", "streaming", "actor", "director", "album", "concert",
        "disney", "hollywood", "star"
    ]
}


# STEP 3: Create helper functions 

def get_top_stories(limit=500):
    """
    Function to fetch list of top story IDs from HackerNews
    
    What it does:
    - Sends a request to HackerNews API
    - Gets the IDs of trending stories
    - Returns first 500 IDs
    
    Parameters:
    - limit: how many story IDs to fetch (default 500)
    
    Returns:
    - List of story IDs
    """
    try:
        print(" Fetching top story IDs from HackerNews...")
        response = requests.get(TOP_STORIES_URL, headers=HEADERS, timeout=10)
        
        # Check if request was successful
        if response.status_code == 200:
            story_ids = response.json()[:limit]
            print(f" Found {len(story_ids)} stories")
            return story_ids
        else:
            print(f" Error: {response.status_code}")
            return []
            
    except Exception as e:
        print(f" Error fetching stories: {e}")
        return []


def get_story_details(story_id):
    """
    Function to fetch details of ONE story
    
    What it does:
    - Fetches the full details of a single story
    - Returns JSON with title, score, author, etc.
    
    Parameters:
    - story_id: the ID of the story to fetch
    
    Returns:
    - Story data as dictionary
    """
    try:
        response = requests.get(
            STORY_URL.format(id=story_id),
            headers=HEADERS,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
            
    except Exception as e:
        print(f" Could not fetch story {story_id}")
        return None


def categorize_story(title):
    """
    Function to assign category to a story based on its title
    
    What it does:
    - Reads the story title
    - Checks if any keywords from our categories appear in title
    - Returns the matching category
    
    Parameters:
    - title: the story title (string)
    
    Returns:
    - category name (string) or "uncategorized"
    """
    # Handle empty titles
    if not title:
        return "uncategorized"
    
    # Convert title to lowercase for matching
    title_lower = title.lower()
    
    # Check each category
    for category, keywords in CATEGORIES.items():
        # Check each keyword in this category
        for keyword in keywords:
            # If keyword found in title, return this category
            if keyword.lower() in title_lower:
                return category
    
    # If no keywords matched, return uncategorized
    return "uncategorized"


def extract_story_fields(story):
    """
    Function to extract the 7 required fields from raw story data
    
    What it does:
    - Takes raw story data from API
    - Extracts only the fields we need
    - Adds a timestamp for when we collected it
    
    Parameters:
    - story: raw story data from API
    
    Returns:
    - Dictionary with 7 fields
    """
    # Handle missing data
    if not story:
        return None
    
    # Extract and return only required fields
    extracted_data = {
        "post_id": story.get("id"),                            # Unique ID
        "title": story.get("title", "N/A"),                    # Story title
        "category": categorize_story(story.get("title", "")),  # Our category
        "score": story.get("score", 0),                        # Number of upvotes
        "num_comments": story.get("descendants", 0),           # Number of comments
        "author": story.get("by", "N/A"),                      # Who wrote it
        "collected_at": datetime.now().isoformat()             # When we collected it
    }
    
    return extracted_data


def save_to_json(stories):
    """
    Function to save collected stories to a JSON file
    
    What it does:
    - Creates a 'data' folder
    - Saves all stories to a JSON file with today's date
    - Prints a summary
    
    Parameters:
    - stories: list of story dictionaries
    
    Returns:
    - filename (string)
    """
    # Create data folder if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create filename with today's date
    # Example: data/trends_20240115.json
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"data/trends_{date_str}.json"
    
    # Write data to file
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(stories, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print(f"\n SUCCESS! Collected {len(stories)} stories")
    print(f" Saved to: {filename}")
    
    return filename


# STEP 4: Main execution
def main():
    """
    Main function - this runs the entire data collection process
    """
    print("=" * 60)
    print(" TRENDPULSE - DATA COLLECTION (TASK 1)")
    print("=" * 60)
    
    # Step 1: Get list of story IDs
    print("\n[Step 1/4] Fetching story IDs...\n")
    story_ids = get_top_stories(limit=500)
    
    if not story_ids:
        print(" Could not fetch stories. Exiting.")
        return
    
    print(f"Total stories found: {len(story_ids)}\n")
    
    # Step 2: Fetch each story
    print("[Step 2/4] Collecting story details...\n")
    print(" This will take 15-20 minutes (fetching 500 stories)...\n")
    
    collected_stories = []
    
    for i, story_id in enumerate(story_ids):
        # Print progress every 50 stories
        if i % 50 == 0 and i > 0:
            print(f"  Progress: {i}/{len(story_ids)} stories fetched...")
        
        # Fetch story details
        story = get_story_details(story_id)
        
        # Extract required fields
        extracted = extract_story_fields(story)
        
        # Add to our collection
        if extracted:
            collected_stories.append(extracted)
        
        # Wait 2 seconds to avoid overwhelming the server
        # (This is polite!)
        time.sleep(2)
    
    print(f"\n Successfully collected {len(collected_stories)} stories\n")
    
    # Step 3: Save to file
    print("[Step 3/4] Saving to JSON file...\n")
    save_to_json(collected_stories)
    
    # Step 4: Show category breakdown
    print("\n[Step 4/4] Category Breakdown:\n")
    category_count = {}
    
    for category in CATEGORIES.keys():
        count = sum(1 for s in collected_stories if s["category"] == category)
        category_count[category] = count
        print(f"  {category.upper()}: {count} stories")
    
    print(f"\n  UNCATEGORIZED: {sum(1 for s in collected_stories if s['category'] == 'uncategorized')} stories")
    
    print("\n" + "=" * 60)
    print(" TASK 1 COMPLETE!")
    print("=" * 60)
    print(f"\n Next: Move to Task 2 - Data Cleaning")
    print("=" * 60 + "\n")


# Run the script
if __name__ == "__main__":
    main()
