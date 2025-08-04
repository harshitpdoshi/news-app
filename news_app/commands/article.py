import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from news_app.services.database import db

console = Console()

@click.group()
def article_group():
    """Manage articles"""
    pass

@article_group.command()
@click.option('--feed-id', type=int, help='Filter by feed ID')
@click.option('--limit', default=20, help='Number of articles to show')
def list(feed_id, limit):
    """List articles"""
    if feed_id:
        articles = db.get_articles_by_feed(feed_id, limit)
        feed = db.get_feed_by_id(feed_id)
        if feed:
            console.print(Panel(f"Articles from: {feed.title}"))
    else:
        articles = db.get_unread_articles(limit)
        console.print(Panel("Unread Articles"))
    
    if not articles:
        console.print("[yellow]No articles found[/yellow]")
        return
    
    table = Table()
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="magenta")
    table.add_column("Feed", style="green")
    table.add_column("Published", style="blue")
    table.add_column("Read", style="yellow")
    
    for article in articles:
        feed = db.get_feed_by_id(article.feed_id)
        feed_title = feed.title if feed else "Unknown"
        
        published = article.published.strftime("%Y-%m-%d %H:%M") if article.published else "Unknown"
        read_status = "Yes" if article.read else "No"
        
        table.add_row(
            str(article.id), 
            article.title, 
            feed_title, 
            published, 
            read_status
        )
    
    console.print(table)

@article_group.command()
@click.argument('article_id', type=int)
def read(article_id):
    """Read an article"""
    # Retrieve the article by ID
    article = db.get_article_by_id(article_id)
    if not article:
        console.print("[red]Article not found[/red]")
        return

    # Mark as read
    db.mark_article_as_read(article_id)

    # Display article content
    feed = db.get_feed_by_id(article.feed_id)
    feed_title = feed.title if feed else "Unknown"

    console.print(Panel(f"[bold]{article.title}[/bold]", subtitle=feed_title))
    if article.author:
        console.print(f"[italic]By {article.author}[/italic]")
    if article.published:
        console.print(f"[blue]Published: {article.published.strftime('%Y-%m-%d %H:%M')}[/blue]")

    console.print("")
    console.print(article.summary if article.summary else "No summary available.")
    console.print("")
    console.print(f"[link={article.link}]Read full article[/link]")
