import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
from datetime import datetime
from news_app.models import Feed, Article
from news_app.services.database import DatabaseService

class TestDatabaseService(unittest.TestCase):
    def setUp(self):
        # Create a temporary database for testing
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_service = DatabaseService(self.temp_db.name)
    
    def tearDown(self):
        # Clean up the temporary database
        os.unlink(self.temp_db.name)
    
    def test_add_feed(self):
        feed = self.db_service.add_feed("https://example.com/rss", "Test Feed", "A test feed")
        self.assertEqual(feed.url, "https://example.com/rss")
        self.assertEqual(feed.title, "Test Feed")
        self.assertEqual(feed.description, "A test feed")
    
    def test_get_all_feeds(self):
        self.db_service.add_feed("https://example.com/rss1", "Test Feed 1")
        self.db_service.add_feed("https://example.com/rss2", "Test Feed 2")
        
        feeds = self.db_service.get_all_feeds()
        self.assertEqual(len(feeds), 2)
    
    def test_add_articles(self):
        # First add a feed
        feed = self.db_service.add_feed("https://example.com/rss", "Test Feed")
        
        # Create test articles
        articles = [
            Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary 1", datetime.now(), "Author 1", False),
            Article(0, feed.id, "Article 2", "https://example.com/article2", "Summary 2", datetime.now(), "Author 2", False)
        ]
        
        added_count = self.db_service.add_articles(articles)
        self.assertEqual(added_count, 2)
    
    def test_get_articles_by_feed(self):
        # First add a feed
        feed = self.db_service.add_feed("https://example.com/rss", "Test Feed")
        
        # Add articles
        articles = [
            Article(0, feed.id, "Article 1", "https://example.com/article1", "Summary 1", datetime.now(), "Author 1", False),
        ]
        
        self.db_service.add_articles(articles)
        
        # Retrieve articles
        retrieved_articles = self.db_service.get_articles_by_feed(feed.id)
        self.assertEqual(len(retrieved_articles), 1)
        self.assertEqual(retrieved_articles[0].title, "Article 1")

if __name__ == '__main__':
    unittest.main()