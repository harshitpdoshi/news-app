import pytest
from datetime import datetime
from news_app.models import Feed, Article

def test_add_feed(temp_db):
    """Test adding a feed to the database"""
    feed = temp_db.add_feed("https://example.com/rss", "Test Feed", "A test feed")
    assert feed.url == "https://example.com/rss"
    assert feed.title == "Test Feed"
    assert feed.description == "A test feed"

def test_get_all_feeds(temp_db):
    """Test retrieving all feeds"""
    temp_db.add_feed("https://example.com/rss1", "Test Feed 1")
    temp_db.add_feed("https://example.com/rss2", "Test Feed 2")
    
    feeds = temp_db.get_all_feeds()
    assert len(feeds) == 2
    assert feeds[0].title == "Test Feed 1"
    assert feeds[1].title == "Test Feed 2"

def test_add_articles(temp_db):
    """Test adding articles to the database"""
    # First add a feed
    feed = temp_db.add_feed("https://example.com/rss", "Test Feed")
    
    # Create test articles
    articles = [
        Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary 1", datetime.now(), "Author 1", False),
        Article(0, feed.id, "Article 2", "https://example.com/article2", "Summary 2", datetime.now(), "Author 2", False)
    ]
    
    added_count = temp_db.add_articles(articles)
    assert added_count == 2

def test_get_articles_by_feed(temp_db):
    """Test retrieving articles by feed"""
    # First add a feed
    feed = temp_db.add_feed("https://example.com/rss", "Test Feed")
    
    # Add articles
    articles = [
        Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary 1", datetime.now(), "Author 1", False),
    ]
    
    temp_db.add_articles(articles)
    
    # Retrieve articles
    retrieved_articles = temp_db.get_articles_by_feed(feed.id)
    assert len(retrieved_articles) == 1
    assert retrieved_articles[0].title == "Article 1"

def test_mark_article_as_read(temp_db):
    """Test marking an article as read"""
    # First add a feed
    feed = temp_db.add_feed("https://example.com/rss", "Test Feed")
    
    # Add an article
    articles = [
        Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary 1", datetime.now(), "Author 1", False),
    ]
    
    temp_db.add_articles(articles)
    
    # Get the article
    retrieved_articles = temp_db.get_articles_by_feed(feed.id)
    article_id = retrieved_articles[0].id
    
    # Mark as read
    result = temp_db.mark_article_as_read(article_id)
    assert result == True
    
    # Check that it's marked as read
    updated_articles = temp_db.get_articles_by_feed(feed.id)
    assert updated_articles[0].read == True

def test_get_article_by_id_and_update_last_updated(temp_db):
    """Test retrieving an article by ID and updating feed last_updated timestamp"""
    # Add a feed and verify last_updated is initially None
    feed = temp_db.add_feed("https://example.com/rss", "Test Feed")
    assert temp_db.get_feed_by_id(feed.id).last_updated is None

    # Add an article and retrieve its ID
    articles = [
        Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary", datetime.now(), "Author", False)
    ]
    temp_db.add_articles(articles)
    retrieved = temp_db.get_articles_by_feed(feed.id)
    assert retrieved
    art_id = retrieved[0].id

    # Test get_article_by_id for existing and non-existing IDs
    article = temp_db.get_article_by_id(art_id)
    assert article is not None and article.id == art_id
    assert temp_db.get_article_by_id(0) is None

    # Update the feed's last_updated timestamp and verify
    ts = datetime.now()
    result = temp_db.update_feed_last_updated(feed.id, ts)
    assert result is True
    updated_feed = temp_db.get_feed_by_id(feed.id)
    assert updated_feed and abs((updated_feed.last_updated - ts).total_seconds()) < 1
