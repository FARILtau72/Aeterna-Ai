import json
import os
import pytest

def test_news_feed_is_static_and_curated():
    """Verify that the dynamic news generator has been disabled and static curated news is used."""
    with open("app.py", "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "generate_dynamic_news_fallback" not in content, "Dynamic fallback generator must be removed"
    assert "Conduit AI" not in content or "DISABLED" in content, "LLM news generation must be disabled or removed"

def test_latest_waste_news_json():
    """Verify the curated news JSON exists and contains valid URLs."""
    news_file = "data/latest_waste_news.json"
    assert os.path.exists(news_file)
    
    with open(news_file, "r", encoding="utf-8") as f:
        articles = json.load(f)
        
    assert len(articles) > 0
    for a in articles:
        assert "url" in a
        assert a["url"].startswith("http")
        assert "title" in a
        assert "source" in a
