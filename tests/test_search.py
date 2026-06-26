import pytest
from app.crawler import Crawler
from app.search_utils import SearchEngine

@pytest.mark.asyncio
async def test_query_scoring():
    crawler = Crawler("./tests/fixtures")
    crawler.documents = {1: "hello world", 2: "hello fastapi", 3: "world search"}
    crawler.index_document(1, crawler.documents[1])
    crawler.index_document(2, crawler.documents[2])
    crawler.index_document(3, crawler.documents[3])
    engine = SearchEngine(crawler)
    results = engine.query("hello")
    assert results[0] == 1 or results[0] == 2
