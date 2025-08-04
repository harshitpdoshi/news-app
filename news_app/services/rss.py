import feedparser
from typing import List, Optional
from datetime import datetime
from news_app.models import Feed, Article
from news_app.services.database import db

class RSSService:
    """Service to handle RSS feed parsing and processing"""
    
    @staticmethod
    def parse_feed(url: str) -> Optional[Feed]:
        """Parse an RSS feed and return feed information"""
        try:
            parsed_feed = feedparser.parse(url)
            
            # Check if feed is valid
            if parsed_feed.bozo:
                # Some feeds have minor issues but are still usable
                # We'll check if we have essential data
                pass
            
            # Check if we have a title
            if not hasattr(parsed_feed.feed, 'title') or not parsed_feed.feed.title:
                return None
                
            feed = Feed(
                id=0,  # Will be set by database
                url=url,
                title=str(parsed_feed.feed.title),
                description=str(getattr(parsed_feed.feed, 'description', '')),
                last_updated=datetime.now()
            )
            
            return feed
        except Exception:
            return None
    
    @staticmethod
    def fetch_articles(feed: Feed) -> List[Article]:
        """Fetch articles from an RSS feed"""
        try:
            parsed_feed = feedparser.parse(feed.url)
            articles = []
            
            for entry in parsed_feed.entries:
                # Parse publication date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6])
                    except Exception:
                        pass
                
                article = Article(
                    id=0,  # Will be set by database
                    feed_id=feed.id,
                    title=str(getattr(entry, 'title', 'Untitled')),
                    link=str(getattr(entry, 'link', '')),
                    summary=str(getattr(entry, 'summary', '')),
                    published=published,
                    author=str(getattr(entry, 'author', '')),
                    read=False
                )
                
                articles.append(article)
            
            return articles
        except Exception:
            return []
    
    @staticmethod
    def update_feed(feed_id: int) -> int:
        """Update a feed by fetching new articles"""
        feed = db.get_feed_by_id(feed_id)
        if not feed:
            return 0
            
        articles = RSSService.fetch_articles(feed)
        added_count = db.add_articles(articles)
        # update last_updated timestamp for this feed
        try:
            db.update_feed_last_updated(feed_id, datetime.now())
        except Exception:
            pass
        return added_count

# Global RSS service instance
rss_service = RSSService()
