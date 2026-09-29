"""
TASK 2: Clean and Process Data
Takes JSON from Task 1 and cleans it (removes duplicates, handles missing data)
Saves as CSV file
"""

import json
import csv
import os
from datetime import datetime


def load_json_data(filename):
    """
    Load stories from JSON file created in Task 1
    
    Parameters:
    - filename: path to JSON file
    
    Returns:
    - List of stories
    """
    print(f" Loading data from {filename}...")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f" Loaded {len(data)} stories\n")
        return data
    
    except FileNotFoundError:
        print(f" File not found: {filename}")
        return []


def remove_duplicates(stories):
    """
    Remove duplicate stories (same post_id)
    
    Parameters:
    - stories: list of story dictionaries
    
    Returns:
    - list without duplicates
    """
    print(" Removing duplicates...")
    
    # Keep track of seen post IDs
    seen_ids = set()
    unique_stories = []
    duplicates = 0
    
    for story in stories:
        post_id = story.get("post_id")
        
        # If we haven't seen this ID before, keep it
        if post_id not in seen_ids:
            seen_ids.add(post_id)
            unique_stories.append(story)
        else:
            # We've seen this before - skip it
            duplicates += 1
    
    print(f" Removed {duplicates} duplicate stories")
    print(f" {len(unique_stories)} unique stories remain\n")
    
    return unique_stories


def handle_missing_values(stories):
    """
    Fix missing values in data
    - Empty titles → "Unknown Title"
    - Missing scores → 0
    - Missing authors → "Anonymous"
    
    Parameters:
    - stories: list of story dictionaries
    
    Returns:
    - cleaned list
    """
    print(" Fixing missing values...")
    
    missing_count = 0
    
    for story in stories:
        # Fix title
        if not story.get("title") or story.get("title") == "N/A":
            story["title"] = "Unknown Title"
            missing_count += 1
        
        # Fix score
        if story.get("score") is None or story.get("score") < 0:
            story["score"] = 0
            missing_count += 1
        
        # Fix author
        if not story.get("author") or story.get("author") == "N/A":
            story["author"] = "Anonymous"
            missing_count += 1
        
        # Fix comments
        if story.get("num_comments") is None or story.get("num_comments") < 0:
            story["num_comments"] = 0
            missing_count += 1
    
    print(f" Fixed {missing_count} missing values\n")
    
    return stories


def remove_low_quality_stories(stories, min_score=0):
    """
    Remove stories with very low engagement
    (Optional - keeps stories with any score)
    
    Parameters:
    - stories: list of stories
    - min_score: minimum score to keep
    
    Returns:
    - filtered list
    """
    print(f" Filtering low-quality stories (score < {min_score})...")
    
    quality_stories = [s for s in stories if s.get("score", 0) >= min_score]
    removed = len(stories) - len(quality_stories)
    
    print(f" Removed {removed} low-quality stories\n")
    
    return quality_stories


def save_to_csv(stories, filename="data/trends_cleaned.csv"):
    """
    Save cleaned data to CSV file
    
    Parameters:
    - stories: list of story dictionaries
    - filename: where to save CSV
    
    Returns:
    - filename
    """
    print(f" Saving to CSV: {filename}...")
    
    # Create data folder
    os.makedirs("data", exist_ok=True)
    
    # Define columns (order matters for CSV)
    fieldnames = [
        "post_id",
        "title",
        "category",
        "score",
        "num_comments",
        "author",
        "collected_at"
    ]
    
    # Write CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        # Write header row
        writer.writeheader()
        
        # Write data rows
        writer.writerows(stories)
    
    print(f" Saved {len(stories)} stories to {filename}\n")
    
    return filename


def print_statistics(stories):
    """
    Print statistics about cleaned data
    
    Parameters:
    - stories: list of stories
    """
    print("\n" + "=" * 60)
    print(" DATA STATISTICS")
    print("=" * 60)
    
    # Total stories
    print(f"\nTotal Stories: {len(stories)}")
    
    # By category
    print("\nStories by Category:")
    categories = {}
    for story in stories:
        cat = story.get("category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat in sorted(categories.keys()):
        print(f"  • {cat}: {categories[cat]}")
    
    # Average score
    avg_score = sum(s.get("score", 0) for s in stories) / len(stories)
    print(f"\nAverage Score: {avg_score:.1f}")
    
    # Average comments
    avg_comments = sum(s.get("num_comments", 0) for s in stories) / len(stories)
    print(f"Average Comments: {avg_comments:.1f}")
    
    # Top 3 stories by score
    top_3 = sorted(stories, key=lambda x: x.get("score", 0), reverse=True)[:3]
    print("\nTop 3 Stories by Score:")
    for i, story in enumerate(top_3, 1):
        print(f"  {i}. {story['title'][:50]}... (Score: {story['score']})")
    
    print("\n" + "=" * 60 + "\n")


# Main Function

def main():
    """
    Main execution - runs full cleaning process
    """
    print("\n" + "=" * 60)
    print("TRENDPULSE - DATA PROCESSING (TASK 2)")
    print("=" * 60 + "\n")
    
    # Step 1: Load data from Task 1
    print("[Step 1/5] Loading JSON data...\n")
    
    # Find the most recent JSON file
    data_files = [f for f in os.listdir("data") if f.startswith("trends_") and f.endswith(".json")]
    
    if not data_files:
        print(" No JSON file found! Run Task 1 first.")
        return
    
    latest_file = os.path.join("data", sorted(data_files)[-1])
    stories = load_json_data(latest_file)
    
    if not stories:
        return
    
    # Step 2: Remove duplicates
    print("[Step 2/5] Cleaning data...\n")
    stories = remove_duplicates(stories)
    
    # Step 3: Fix missing values
    stories = handle_missing_values(stories)
    
    # Step 4: Remove low quality (optional)
    # stories = remove_low_quality_stories(stories, min_score=0)
    
    # Step 5: Save to CSV
    print("[Step 3/5] Saving to CSV...\n")
    csv_filename = save_to_csv(stories)
    
    # Step 6: Print statistics
    print("[Step 4/5] Analyzing cleaned data...\n")
    print_statistics(stories)
    
    print("=" * 60)
    print(" TASK 2 COMPLETE!")
    print("=" * 60)
    print(f"\n Next: Move to Task 3 - Data Analysis")
    print("=" * 60 + "\n")


# Run the script
if __name__ == "__main__":
    main()
