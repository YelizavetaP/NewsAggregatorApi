from typing import List

# Valid Topics
VALID_TOPICS: List[str] = [
    'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 
    'ENTERTAINMENT', 'SCIENCE', 'SPORTS', 
    'HEALTH'
]

VALID_GEO_LOCATIONS: List[str] = ['NY']

# RSS Feed Configuration
GOOGLE_NEWS_BASE_URL = "https://news.google.com/rss/headlines/section/"
# GOOGLE_NEWS_BASE_URL = "https://news.google.com/rss/headlines/section/topic/"


# Article Limits
ARTICLES_PER_TOPIC = 5
