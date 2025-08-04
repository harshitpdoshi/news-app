import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from news_app.services.database import db
from news_app.services.rss import rss_service
from datetime import datetime

console = Console()

@click.group()
def feed_group():
    """Manage RSS feeds"""
    pass

@feed_group.command()
@click.argument('url')
def add(url):
    """Add a new RSS feed"""
    feed = rss_service.parse_feed(url)
    if not feed:
        console.print(f"[red]Error: Could not parse feed from {url}[/red]")
        return
    
    try:
        saved_feed = db.add_feed(feed.url, feed.title, feed.description)
        console.print(f"[green]Successfully added feed:[/green] {saved_feed.title}")
        
        # Fetch initial articles
        articles = rss_service.fetch_articles(saved_feed)
        added_count = db.add_articles(articles)
        console.print(f"[green]Added {added_count} articles from {saved_feed.title}[/green]")
        # update last_updated timestamp for this feed
        db.update_feed_last_updated(saved_feed.id, datetime.now())
    except Exception as e:
        console.print(f"[red]Error adding feed: {str(e)}[/red]")

@feed_group.command()
def list():
    """List all RSS feeds"""
    feeds = db.get_all_feeds()
    
    if not feeds:
        console.print("[yellow]No feeds found. Add a feed with: news-app feed add <url>[/yellow]")
        return
    
    table = Table(title="RSS Feeds")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("URL", style="green")
    table.add_column("Articles", style="blue")
    
    for feed in feeds:
        # Count articles for this feed
        articles = db.get_articles_by_feed(feed.id)
        table.add_row(str(feed.id), feed.title, feed.url, str(len(articles)))
    
    console.print(table)

@feed_group.command()
@click.argument('feed_id', type=int)
def update(feed_id):
    """Update a specific feed"""
    added_count = rss_service.update_feed(feed_id)
    if added_count > 0:
        console.print(f"[green]Added {added_count} new articles[/green]")
    else:
        console.print("[yellow]No new articles found[/yellow]")

@feed_group.command()
@click.argument('feed_id', type=int)
def delete(feed_id):
    """Delete a feed and all its articles"""
    feed = db.get_feed_by_id(feed_id)
    if not feed:
        console.print("[red]Feed not found[/red]")
        return
    
    if db.delete_feed(feed_id):
        console.print(f"[green]Deleted feed: {feed.title}[/green]")
    else:
        console.print("[red]Error deleting feed[/red]")

@feed_group.command()
def update_all():
    """Update all feeds"""
    feeds = db.get_all_feeds()
    if not feeds:
        console.print("[yellow]No feeds to update[/yellow]")
        return
    
    total_added = 0
    for feed in feeds:
        added_count = rss_service.update_feed(feed.id)
        total_added += added_count
        if added_count > 0:
            console.print(f"[green]Added {added_count} articles from {feed.title}[/green]")
    
    if total_added == 0:
        console.print("[yellow]No new articles found in any feeds[/yellow]")
