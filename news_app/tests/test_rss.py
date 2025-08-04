import pytest
from unittest.mock import patch, MagicMock, ANY
from datetime import datetime
from news_app.models import Feed
from news_app.services.rss import RSSService

@patch('news_app.services.rss.feedparser.parse')
def test_parse_feed(mock_parse):
    """Test parsing an RSS feed"""
    # Mock the feedparser response
    mock_feed_obj = MagicMock()
    mock_feed_obj.title = "Test Feed"
    mock_feed_obj.description = "A test feed"
    
    mock_feed_data = MagicMock()
    mock_feed_data.bozo = False
    mock_feed_data.feed = mock_feed_obj
    mock_parse.return_value = mock_feed_data
    
    feed = RSSService.parse_feed("https://example.com/rss")
    assert feed is not None
    assert feed.title == "Test Feed"
    assert feed.description == "A test feed"

@patch('news_app.services.rss.feedparser.parse')
def test_parse_feed_with_bozo_exception(mock_parse):
    """Test parsing an RSS feed with bozo exception"""
    # Mock the feedparser response with bozo exception
    mock_feed_obj = MagicMock()
    mock_feed_obj.title = "Test Feed"
    mock_feed_obj.description = "A test feed"
    
    mock_feed_data = MagicMock()
    mock_feed_data.bozo = True
    mock_feed_data.bozo_exception = Exception("Parse error")
    mock_feed_data.feed = mock_feed_obj
    mock_parse.return_value = mock_feed_data
    
    feed = RSSService.parse_feed("https://example.com/rss")
    assert feed is not None  # Should still work with bozo flag

@patch('news_app.services.rss.feedparser.parse')
def test_fetch_articles(mock_parse):
    """Test fetching articles from an RSS feed"""
    # Mock the feedparser response
    mock_entry = MagicMock()
    mock_entry.title = "Test Article"
    mock_entry.link = "https://example.com/article"
    mock_entry.summary = "Test summary"
    mock_entry.published_parsed = (2023, 1, 1, 12, 0, 0, 0, 0, 0)
    mock_entry.author = "Test Author"
    
    mock_feed_data = MagicMock()
    mock_feed_data.entries = [mock_entry]
    mock_feed_data.bozo = False
    mock_parse.return_value = mock_feed_data
    
    # Create a test feed
    feed = Feed(1, "https://example.com/rss", "Test Feed")
    
    articles = RSSService.fetch_articles(feed)
    assert len(articles) == 1
    assert articles[0].title == "Test Article"
    assert articles[0].link == "https://example.com/article"
    assert articles[0].summary == "Test summary"
    assert articles[0].author == "Test Author"


@patch('news_app.services.rss.db')
def test_update_feed_not_found(mock_db):
    """Test updating a non-existent feed returns zero"""
    mock_db.get_feed_by_id.return_value = None
    added = RSSService.update_feed(999)
    assert added == 0
    mock_db.get_feed_by_id.assert_called_once_with(999)


@patch('news_app.services.rss.RSSService.fetch_articles')
@patch('news_app.services.rss.db')
def test_update_feed_updates_timestamp(mock_db, mock_fetch):
    """Test updating a feed adds articles and updates last_updated"""
    feed = Feed(1, "https://example.com/rss", "Test Feed")
    mock_db.get_feed_by_id.return_value = feed
    mock_fetch.return_value = []
    mock_db.add_articles.return_value = 0

    added = RSSService.update_feed(feed.id)
    assert added == 0
    mock_db.add_articles.assert_called_once_with([])
    mock_db.update_feed_last_updated.assert_called_once_with(feed.id, ANY)
