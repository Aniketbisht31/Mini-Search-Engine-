import math
from collections import defaultdict
from app.crawler import Crawler

class SearchEngine:
    def __init__(self, crawler: Crawler):
        self.crawler = crawler
        self.tfidf = crawler.compute_tfidf()
        self.page_rank = crawler.build_page_rank()

    def query(self, text: str):
        tokens = self.crawler.normalize(text)
        scores = defaultdict(float)
        for token in tokens:
            postings = self.crawler.inverted_index.get(token, {})
            for doc_id, _ in postings.items():
                tfidf_score = self.tfidf[doc_id].get(token, 0.0)
                scores[doc_id] += tfidf_score
        ranked = sorted(scores.items(), key=lambda item: (item[1], self.page_rank.get(item[0], 0.0)), reverse=True)
        return [doc_id for doc_id, _ in ranked]
