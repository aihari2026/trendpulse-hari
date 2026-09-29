"""
TASK 4: Create Visualizations
Generate charts to show trends visually
"""

import csv


def load_csv_data(filename="data/trends_cleaned.csv"):
    """Load CSV data"""
    print(f" Loading data from {filename}...\n")
    
    stories = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                row["score"] = int(row["score"])
                row["num_comments"] = int(row["num_comments"])
                stories.append(row)
        
        print(f" Loaded {len(stories)} stories\n")
        return stories
    
    except FileNotFoundError:
        print(f" File not found: {filename}")
        return []


def create_text_chart(stories):
    """
    Create a simple text-based chart
    (No external libraries needed!)
    """
    print("=" * 60)
    print(" CATEGORY DISTRIBUTION (Text Chart)")
    print("=" * 60 + "\n")
    
    # Count stories by category
    categories = {}
    for story in stories:
        cat = story["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    # Find max count for scaling
    max_count = max(categories.values())
    
    # Create chart
    for category in sorted(categories.keys()):
        count = categories[category]
        # Scale count to bar length (max 40 characters)
        bar_length = int((count / max_count) * 40)
        bar = " " * bar_length
        percentage = (count / len(stories)) * 100
        
        print(f"{category:15} | {bar} {count:3} ({percentage:5.1f}%)")
    
    print()


def create_score_distribution(stories):
    """
    Create score distribution chart
    """
    print("=" * 60)
    print(" SCORE DISTRIBUTION")
    print("=" * 60 + "\n")
    
    # Create buckets (ranges)
    # 0-10, 11-50, 51-100, 101-200, 200+
    buckets = {
        "0-10": 0,
        "11-50": 0,
        "51-100": 0,
        "101-200": 0,
        "200+": 0
    }
    
    # Place stories into buckets
    for story in stories:
        score = story["score"]
        if score <= 10:
            buckets["0-10"] += 1
        elif score <= 50:
            buckets["11-50"] += 1
        elif score <= 100:
            buckets["51-100"] += 1
        elif score <= 200:
            buckets["101-200"] += 1
        else:
            buckets["200+"] += 1
    
    # Draw chart
    max_count = max(buckets.values())
    for range_name, count in buckets.items():
        bar_length = int((count / max_count) * 30)
        bar = " " * bar_length
        print(f"Score {range_name:10} | {bar} {count}")
    
    print()


def create_author_stats(stories, top_n=10):
    """
    Find most active authors
    """
    print("=" * 60)
    print(f"  TOP {top_n} ACTIVE AUTHORS")
    print("=" * 60 + "\n")
    
    # Count stories per author
    authors = {}
    for story in stories:
        author = story["author"]
        authors[author] = authors.get(author, 0) + 1
    
    # Sort by count
    sorted_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)
    
    # Show top authors
    for i, (author, count) in enumerate(sorted_authors[:top_n], 1):
        bar = "★" * count
        print(f"{i:2}. {author:20} | {bar} ({count})")
    
    print()


def create_summary_report(stories):
    """
    Create a complete summary report
    """
    print("\n" + "=" * 60)
    print(" SUMMARY REPORT")
    print("=" * 60 + "\n")
    
    # Category breakdown
    print("Stories by Category:")
    categories = {}
    for story in stories:
        cat = story["category"]
        categories[cat] = categories.get(cat, 0) + 1
    
    for cat in sorted(categories.keys()):
        pct = (categories[cat] / len(stories)) * 100
        print(f"  • {cat:15} : {categories[cat]:3} stories ({pct:5.1f}%)")
    
    # Score statistics
    scores = [int(s["score"]) for s in stories]
    print(f"\nScore Statistics:")
    print(f"  • Minimum   : {min(scores)}")
    print(f"  • Maximum   : {max(scores)}")
    print(f"  • Average   : {sum(scores)/len(scores):.1f}")
    print(f"  • Median    : {sorted(scores)[len(scores)//2]}")
    
    # Comments statistics
    comments = [int(s["num_comments"]) for s in stories]
    print(f"\nComments Statistics:")
    print(f"  • Minimum   : {min(comments)}")
    print(f"  • Maximum   : {max(comments)}")
    print(f"  • Average   : {sum(comments)/len(comments):.1f}")
    
    print()


# Main Function

def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print(" TRENDPULSE - DATA VISUALIZATION (TASK 4)")
    print("=" * 60 + "\n")
    
    # Load data
    print("[Step 1/5] Loading cleaned data...\n")
    stories = load_csv_data()
    
    if not stories:
        return
    
    # Create visualizations
    print("[Step 2/5] Creating visualizations...\n")
    
    create_text_chart(stories)
    create_score_distribution(stories)
    create_author_stats(stories, top_n=5)
    create_summary_report(stories)
    
    print("=" * 60)
    print(" TASK 4 COMPLETE!")
    print("=" * 60)
    print("\n ALL TASKS FINISHED!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
