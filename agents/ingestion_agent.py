import json

class ReviewIngestionAgent:
    def __init__(self, data_path):
        with open(data_path, "r") as f:
            self.reviews = json.load(f)

    def get_reviews_by_date(self, date):
        return [r for r in self.reviews if r["date"] == date]
