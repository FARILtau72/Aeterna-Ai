"""
AETERNA AI — News Service (Curated Static Mode)
"""

import os
import json
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

def get_curated_news() -> Dict[str, Any]:
    """Retrieve curated, manually-verified news articles about waste management in Jakarta."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    news_file = os.path.join(base_dir, "data", "latest_waste_news.json")

    curated_metadata = {
        "data_source": "curated_static",
        "disclaimer": "Articles are manually curated references to real published content. Not a live news feed. LLM article generation is disabled.",
        "last_curated": "2026-07-20"
    }

    if os.path.exists(news_file):
        try:
            with open(news_file, "r", encoding="utf-8") as f:
                articles = json.load(f)
            if isinstance(articles, list) and len(articles) > 0:
                seen_urls = set()
                unique_articles = []
                for a in articles:
                    url = a.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        unique_articles.append(a)
                return {
                    "status": "ok",
                    "articles": unique_articles,
                    **curated_metadata
                }
        except Exception as e:
            logger.error(f"Failed to read curated news: {e}")

    return {
        "status": "no_updates",
        "articles": [],
        "message": "No verified updates available. Check back later.",
        **curated_metadata
    }
