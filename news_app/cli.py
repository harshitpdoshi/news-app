#!/usr/bin/env python3

import click
from rich.console import Console

from news_app.commands.feed import feed_group
from news_app.commands.article import article_group

console = Console()

@click.group()
def cli():
    """News App - A CLI RSS feed reader"""
    pass

cli.add_command(feed_group)
cli.add_command(article_group)

if __name__ == '__main__':
    cli()