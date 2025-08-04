import sqlite3
import os
from typing import List, Optional
from datetime import datetime
from news_app.models import Feed, Article

class DatabaseService:
    """Service to handle database operations for feeds and articles"""
    
    def __init__(self, db_path: str = "feeds.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database with required tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create feeds table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS feeds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    last_updated TIMESTAMP
                )
            ''')
            
            # Create articles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    feed_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    link TEXT NOT NULL,
                    summary TEXT,
                    published TIMESTAMP,
                    author TEXT,
                    read BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (feed_id) REFERENCES feeds (id)
                )
            ''')
            
            # Create unique index on articles link to prevent duplicates
            cursor.execute('''
                CREATE UNIQUE INDEX IF NOT EXISTS idx_articles_link 
                ON articles (link)
            ''')
            
            conn.commit()
    
    def add_feed(self, url: str, title: str, description: str = "") -> Feed:
        """Add a new feed to the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO feeds (url, title, description, last_updated)
                VALUES (?, ?, ?, ?)
            ''', (url, title, description, None))
            
            # Get the inserted or existing feed
            cursor.execute('SELECT id, url, title, description, last_updated FROM feeds WHERE url = ?', (url,))
            row = cursor.fetchone()
            
            if row[4]:  # last_updated
                last_updated = datetime.fromisoformat(row[4])
            else:
                last_updated = None
                
            return Feed(id=row[0], url=row[1], title=row[2], description=row[3], last_updated=last_updated)
    
    def get_all_feeds(self) -> List[Feed]:
        """Get all feeds from the database"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, url, title, description, last_updated FROM feeds')
            rows = cursor.fetchall()
            
            feeds = []
            for row in rows:
                if row[4]:  # last_updated
                    last_updated = datetime.fromisoformat(row[4])
                else:
                    last_updated = None
                    
                feeds.append(Feed(id=row[0], url=row[1], title=row[2], description=row[3], last_updated=last_updated))
            
            return feeds
    
    def get_feed_by_id(self, feed_id: int) -> Optional[Feed]:
        """Get a feed by its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, url, title, description, last_updated FROM feeds WHERE id = ?', (feed_id,))
            row = cursor.fetchone()
            
            if row:
                if row[4]:  # last_updated
                    last_updated = datetime.fromisoformat(row[4])
                else:
                    last_updated = None
                    
                return Feed(id=row[0], url=row[1], title=row[2], description=row[3], last_updated=last_updated)
            return None
    
    def delete_feed(self, feed_id: int) -> bool:
        """Delete a feed and its articles"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM articles WHERE feed_id = ?', (feed_id,))
            result = cursor.execute('DELETE FROM feeds WHERE id = ?', (feed_id,))
            conn.commit()
            return result.rowcount > 0
    
    def add_articles(self, articles: List[Article]) -> int:
        """Add articles to the database, ignoring duplicates"""
        added_count = 0
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            for article in articles:
                try:
                    published_str = article.published.isoformat() if article.published else None
                    cursor.execute('''
                        INSERT INTO articles (feed_id, title, link, summary, published, author, read)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        article.feed_id, 
                        article.title, 
                        article.link, 
                        article.summary, 
                        published_str, 
                        article.author,
                        article.read
                    ))
                    added_count += 1
                except sqlite3.IntegrityError:
                    # Article already exists (duplicate link)
                    continue
            conn.commit()
        return added_count
    
    def get_articles_by_feed(self, feed_id: int, limit: int = 50) -> List[Article]:
        """Get articles for a specific feed"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, feed_id, title, link, summary, published, author, read 
                FROM articles 
                WHERE feed_id = ? 
                ORDER BY published DESC 
                LIMIT ?
            ''', (feed_id, limit))
            rows = cursor.fetchall()
            
            articles = []
            for row in rows:
                if row[5]:  # published
                    published = datetime.fromisoformat(row[5])
                else:
                    published = None
                    
                articles.append(Article(
                    id=row[0],
                    feed_id=row[1],
                    title=row[2],
                    link=row[3],
                    summary=row[4],
                    published=published,
                    author=row[6],
                    read=bool(row[7])
                ))
            
            return articles
    
    def get_unread_articles(self, limit: int = 50) -> List[Article]:
        """Get all unread articles"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, feed_id, title, link, summary, published, author, read 
                FROM articles 
                WHERE read = 0
                ORDER BY published DESC 
                LIMIT ?
            ''', (limit,))
            rows = cursor.fetchall()
            
            articles = []
            for row in rows:
                if row[5]:  # published
                    published = datetime.fromisoformat(row[5])
                else:
                    published = None
                    
                articles.append(Article(
                    id=row[0],
                    feed_id=row[1],
                    title=row[2],
                    link=row[3],
                    summary=row[4],
                    published=published,
                    author=row[6],
                    read=bool(row[7])
                ))
            
            return articles
    
    def mark_article_as_read(self, article_id: int) -> bool:
        """Mark an article as read"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE articles SET read = 1 WHERE id = ?', (article_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_article_by_id(self, article_id: int) -> Optional[Article]:
        """Get an article by its ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'SELECT id, feed_id, title, link, summary, published, author, read FROM articles WHERE id = ?',
                (article_id,)
            )
            row = cursor.fetchone()
            if not row:
                return None
            published = datetime.fromisoformat(row[5]) if row[5] else None
            return Article(
                id=row[0],
                feed_id=row[1],
                title=row[2],
                link=row[3],
                summary=row[4],
                published=published,
                author=row[6],
                read=bool(row[7])
            )

    def update_feed_last_updated(self, feed_id: int, timestamp: datetime) -> bool:
        """Update the last_updated timestamp for a feed"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                'UPDATE feeds SET last_updated = ? WHERE id = ?',
                (timestamp.isoformat(), feed_id)
            )
            conn.commit()
            return cursor.rowcount > 0

# Global database instance
db = DatabaseService()
