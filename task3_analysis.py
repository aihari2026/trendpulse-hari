"""
TASK 3: Analyze Data with NumPy and Pandas
Find trends and patterns in the cleaned data
"""

import csv
import os


def load_csv_data(filename="data/trends_cleaned.csv"):
    """Load stories from CSV file"""
    print(f" Loading data from {filename}...")
    
    stories = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numbers to integers
                row["score"] = int(row["score"])
                row["num_comments"] = int(row["num_comments"])
                row["post_id"] = int(row["post_id"])
                stories.append(row)
        
        print(f" Loaded {len(stories)} stories\n")
        return stories
    
    except FileNotFoundError:
        print(f" File not found: {filename}")
        return []


def analyze_by_category(stories):
    """Analyze trends by category"""
    print("\n" + "=" * 60)
    print(" ANALYSIS BY CATEGORY")
    print("=" * 60 + "\n")
    
    categories = {}
    
    # Group stories by category
    for story in stories:
        cat = story["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(story)
    
    results = []
    
    # Analyze each category
    for category in sorted(categories.keys()):
        cat_stories = categories[category]
        
        # Calculate statistics
        count = len(cat_stories)
        avg_score = sum(s["score"] for s in cat_stories) / count
        avg_comments = sum(s["num_comments"] for s in cat_stories) / count
        max_score = max(s["score"] for s in cat_stories)
        min_score = min(s["score"] for s in cat_stories)
        
        result = {
            "category": category,
            "count": count,
            "avg_score": avg_score,
            "avg_comments": avg_comments,
            "max_score": max_score,
            "min_score": min_score
        }
        results.append(result)
        
        # Print results
        print(f"   {category.upper()}")
        print(f"   • Count: {count} stories")
        print(f"   • Avg Score: {avg_score:.1f}")
        print(f"   • Avg Comments: {avg_comments:.1f}")
        print(f"   • Max Score: {max_score}")
        print(f"   • Min Score: {min_score}")
        print()
    
    return results, categories


def find_top_stories(stories, top_n=10):
    """Find top stories by score"""
    print("=" * 60)
    print(f" TOP {top_n} STORIES BY SCORE")
    print("=" * 60 + "\n")
    
    # Sort by score (highest first)
    sorted_stories = sorted(stories, key=lambda x: x["score"], reverse=True)
    
    results = []
    
    for i, story in enumerate(sorted_stories[:top_n], 1):
        title = story["title"][:60]  # First 60 characters
        print(f"{i}. {title}...")
        print(f"   Category: {story['category'].upper()}")
        print(f"   Score: {story['score']} | Comments: {story['num_comments']}")
        print(f"   Author: {story['author']}")
        print()
        
        results.append(story)
    
    return results


def find_most_commented(stories, top_n=10):
    """Find most commented stories"""
    print("=" * 60)
    print(f" TOP {top_n} MOST DISCUSSED STORIES")
    print("=" * 60 + "\n")
    
    # Sort by comments (highest first)
    sorted_stories = sorted(stories, key=lambda x: x["num_comments"], reverse=True)
    
    results = []
    
    for i, story in enumerate(sorted_stories[:top_n], 1):
        title = story["title"][:60]
        print(f"{i}. {title}...")
        print(f"   Category: {story['category'].upper()}")
        print(f"   Comments: {story['num_comments']} | Score: {story['score']}")
        print(f"   Author: {story['author']}")
        print()
        
        results.append(story)
    
    return results


def calculate_overall_stats(stories):
    """Calculate overall statistics"""
    print("=" * 60)
    print(" OVERALL STATISTICS")
    print("=" * 60 + "\n")
    
    total = len(stories)
    
    # Score statistics
    scores = [s["score"] for s in stories]
    avg_score = sum(scores) / total
    max_score = max(scores)
    min_score = min(scores)
    median_score = sorted(scores)[total // 2]
    
    # Comments statistics
    comments = [s["num_comments"] for s in stories]
    avg_comments = sum(comments) / total
    max_comments = max(comments)
    median_comments = sorted(comments)[total // 2]
    
    # Engagement (score + comments)
    engagements = [s["score"] + s["num_comments"] for s in stories]
    avg_engagement = sum(engagements) / total
    
    print(f"Total Stories: {total}")
    print()
    
    print("SCORE Statistics:")
    print(f"  • Average: {avg_score:.1f}")
    print(f"  • Median: {median_score:.1f}")
    print(f"  • Maximum: {max_score}")
    print(f"  • Minimum: {min_score}")
    print()
    
    print("COMMENTS Statistics:")
    print(f"  • Average: {avg_comments:.1f}")
    print(f"  • Median: {median_comments:.1f}")
    print(f"  • Maximum: {max_comments}")
    print()
    
    print("ENGAGEMENT (Score + Comments):")
    print(f"  • Average: {avg_engagement:.1f}")
    print()
    
    return {
        "total": total,
        "avg_score": avg_score,
        "avg_comments": avg_comments,
        "avg_engagement": avg_engagement
    }


def save_analysis_report(cat_results, top_stories, most_commented, overall_stats):
    """Save analysis report to text file"""
    print("\n Saving analysis report...\n")
    
    os.makedirs("data", exist_ok=True)
    filename = "data/analysis_report.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("TRENDPULSE - DATA ANALYSIS REPORT\n")
        f.write("=" * 60 + "\n\n")
        
        # Overall stats
        f.write("OVERALL STATISTICS\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total Stories: {overall_stats['total']}\n")
        f.write(f"Average Score: {overall_stats['avg_score']:.1f}\n")
        f.write(f"Average Comments: {overall_stats['avg_comments']:.1f}\n")
        f.write(f"Average Engagement: {overall_stats['avg_engagement']:.1f}\n\n")
        
        # Category analysis
        f.write("ANALYSIS BY CATEGORY\n")
        f.write("-" * 60 + "\n")
        for result in cat_results:
            f.write(f"\n{result['category'].upper()}\n")
            f.write(f"  Count: {result['count']}\n")
            f.write(f"  Avg Score: {result['avg_score']:.1f}\n")
            f.write(f"  Avg Comments: {result['avg_comments']:.1f}\n")
        
        f.write("\n\n")
    
    print(f" Report saved to {filename}")
    return filename


#  Main Function

def main():
    """Main execution"""
    print("\n" + "=" * 60)
    print(" TRENDPULSE - DATA ANALYSIS (TASK 3)")
    print("=" * 60 + "\n")
    
    # Load data
    print("[Step 1/5] Loading cleaned data...\n")
    stories = load_csv_data()
    
    if not stories:
        return
    
    # Analyze by category
    print("[Step 2/5] Analyzing by category...\n")
    cat_results, categories = analyze_by_category(stories)
    
    # Find top stories
    print("\n[Step 3/5] Finding top stories...\n")
    top_stories = find_top_stories(stories, top_n=10)
    
    # Find most commented
    print("\n[Step 4/5] Finding most discussed stories...\n")
    most_commented = find_most_commented(stories, top_n=10)
    
    # Calculate overall stats
    print("\n[Step 5/5] Calculating overall statistics...\n")
    overall_stats = calculate_overall_stats(stories)
    
    # Save report
    save_analysis_report(cat_results, top_stories, most_commented, overall_stats)
    
    print("\n" + "=" * 60)
    print(" TASK 3 COMPLETE!")
    print("=" * 60)
    print(f"\n Next: Move to Task 4 - Data Visualization")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
