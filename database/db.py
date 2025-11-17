mock_categories = {
    "c1": {"category_id": "c1", "name": "Tutorial"},
    "c2": {"category_id": "c2", "name": "Berita Teknologi"},
}

mock_tags = {
    "t1": {"tag_id": "t1", "name": "python"},
    "t2": {"tag_id": "t2", "name": "fastapi"},
    "t3": {"tag_id": "t3", "name": "ddd"},
}

mock_articles = {
    "a1": {
        "article_id": "a1", "title": "Tutorial FastAPI Lengkap",
        "publish_date": "2025-11-15", "snippet": "Belajar FastAPI dari nol...",
        "category": mock_categories["c1"], 
        "tags": [mock_tags["t1"], mock_tags["t2"]] 
    },
    "a2": {
        "article_id": "a2", "title": "Pentingnya DDD dalam Sistem",
        "publish_date": "2025-11-16", "snippet": "Domain-Driven Design adalah...",
        "category": mock_categories["c1"],
        "tags": [mock_tags["t3"]]
    },
    "a3": {
        "article_id": "a3", "title": "Rilis Python 3.14",
        "publish_date": "2025-11-17", "snippet": "Python rilis versi baru...",
        "category": mock_categories["c2"],
        "tags": [mock_tags["t1"]]
    }
}