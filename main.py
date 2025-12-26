from agents.ingestion_agent import ReviewIngestionAgent
from agents.understanding_agent import ReviewUnderstandingAgent
from agents.canonicalization_agent import TopicCanonicalizationAgent
from agents.aggregation_agent import AggregationAgent
from agents.report_agent import ReportAgent

from datetime import datetime, timedelta
from tqdm import tqdm

TARGET_DATE = "2025-06-30"
START_DATE = (datetime.fromisoformat(TARGET_DATE) - timedelta(days=30)).date()

ingestor = ReviewIngestionAgent("data/reviews_raw.json")
understander = ReviewUnderstandingAgent()
canonicalizer = TopicCanonicalizationAgent("memory/topic_store.json")
aggregator = AggregationAgent(START_DATE, TARGET_DATE)
reporter = ReportAgent()

current = START_DATE
while current <= datetime.fromisoformat(TARGET_DATE).date():
    daily_reviews = ingestor.get_reviews_by_date(str(current))

    for review in tqdm(daily_reviews, desc=str(current)):
        topics = understander.extract_topics(review["text"])
        canonical_topics = [canonicalizer.canonicalize(t) for t in topics]
        aggregator.add_topics(str(current), canonical_topics)

    current += timedelta(days=1)

df = aggregator.to_dataframe()
reporter.save(df, f"output/trend_report_{TARGET_DATE}.csv")
