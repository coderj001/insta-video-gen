import csv
from src.settings import settings
from collections import Counter


def get_all_tags() -> list[str]:
    # Read the CSV file
    with open('instagram_metadata.csv', 'r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]

    # Sort the rows based on Likes and Comments
    # (convert to integers for proper sorting)
    sorted_rows = sorted(rows, key=lambda x: (
        int(x['Likes']), int(x['Comments'])), reverse=True)

    # Extract hashtags from the sorted rows
    all_hashtags = []
    for row in sorted_rows:
        hashtags = row['Hashtags'].split()
        all_hashtags.extend(hashtags)

    # Get the 20 most common hashtags
    top_tags = [tag for tag, _ in Counter(
        all_hashtags).most_common(settings.limit_hashtags)]

    return settings.imp_hashtags + top_tags
