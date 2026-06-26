import os
import math
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()

class Crawler:
    def __init__(self, root: str):
        self.root = Path(root)
        self.documents: Dict[int, str] = {}
        self.inverted_index: Dict[str, Dict[int, int]] = defaultdict(dict)
        self.page_rank: Dict[int, float] = {}
        self.links: Dict[int, List[int]] = defaultdict(list)

    def normalize(self, text: str) -> List[str]:
        tokens = [token.lower() for token in word_tokenize(text) if token.isalpha()]
        return [STEMMER.stem(token) for token in tokens if token not in STOP_WORDS]

    def crawl_files(self):
        for path in self.root.rglob("*.txt"):
            doc_id = len(self.documents) + 1
            self.documents[doc_id] = path.read_text(encoding="utf-8")
            self.index_document(doc_id, self.documents[doc_id])
        return self.documents

    def index_document(self, doc_id: int, content: str):
        tokens = self.normalize(content)
        for token in tokens:
            self.inverted_index[token][doc_id] = self.inverted_index[token].get(doc_id, 0) + 1

    def compute_tfidf(self) -> Dict[int, Dict[str, float]]:
        doc_count = len(self.documents)
        tfidf_scores: Dict[int, Dict[str, float]] = {doc_id: {} for doc_id in self.documents}
        for term, postings in self.inverted_index.items():
            df = len(postings)
            idf = math.log((doc_count / (1 + df)))
            for doc_id, tf in postings.items():
                tfidf_scores[doc_id][term] = (1 + math.log(tf)) * idf
        return tfidf_scores

    def build_page_rank(self, iterations: int = 20, damping: float = 0.85):
        n = len(self.documents)
        if n == 0:
            return {}
        self.page_rank = {doc_id: 1.0 / n for doc_id in self.documents}
        for _ in range(iterations):
            new_rank = {doc_id: (1 - damping) / n for doc_id in self.documents}
            for doc_id, outgoing in self.links.items():
                share = self.page_rank[doc_id] / max(len(outgoing), 1)
                for target in outgoing:
                    new_rank[target] += damping * share
            self.page_rank = new_rank
        return self.page_rank
