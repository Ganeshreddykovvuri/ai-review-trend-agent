from google_play_scraper import reviews, Sort
from datetime import datetime
import json
import os

APP_ID = "in.swiggy.android"   # Change for other apps
MAX_REVIEWS = 200              # Fetch latest 200 reviews

DATA_FILE = "data/reviews_raw.json"

def fetch_today_reviews():
    result, _ = reviews(
        APP_ID,
        lang="en",
        country="in",
        sort=Sort.NEWEST,
        count=MAX_REVIEWS
    )

    today = datetime.today().date().isoformat()
    todays_reviews = []

    for r in result:
        review_date = r["at"].date().isoformat()
        if review_date == today:
            todays_reviews.append({
                "date": review_date,
                "text": r["content"]
            })

    return todays_reviews

def load_existing():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_reviews(reviews):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    existing = load_existing()
    new_reviews = fetch_today_reviews()

    combined = existing + new_reviews
    save_reviews(combined)

    print(f"Fetched {len(new_reviews)} new reviews for today")
