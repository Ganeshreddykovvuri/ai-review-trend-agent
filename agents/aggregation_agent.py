import pandas as pd
from collections import defaultdict

class AggregationAgent:
    def __init__(self, start_date, end_date):
        # Store all dates as strings
        self.dates = pd.date_range(start_date, end_date).astype(str)
        self.matrix = defaultdict(lambda: defaultdict(int))

    def add_topics(self, date, topics):
        for topic in topics:
            self.matrix[topic][date] += 1

    def to_dataframe(self):
        # Create dataframe from collected counts
        df = pd.DataFrame(self.matrix).T

        # Ensure all dates exist as columns
        for date in self.dates:
            if date not in df.columns:
                df[date] = 0

        # Order columns chronologically and fill missing values
        df = df[self.dates].fillna(0)

        return df
