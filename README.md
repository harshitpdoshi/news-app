# News App - CLI RSS Reader

A command-line RSS feed reader built with Python, Click, and Rich.

## Features

- Add and manage RSS feeds
- Fetch and read articles from feeds
- Mark articles as read
- View unread articles
- AI-powered article summarization
- Update feeds to get new articles

## Installation

Make sure you have `uv` installed:

```bash
pip install uv
```

- Install dependencies:

```bash
uv sync
```

## Usage

### Adding a feed

```bash
news-app feed add https://feeds.bbci.co.uk/news/rss.xml
```

### Listing feeds

```bash
news-app feed list
```

### Updating feeds

Update a specific feed:
```bash
news-app feed update 1
```

Update all feeds:
```bash
news-app feed update-all
```

### Listing articles

List unread articles:
```bash
news-app article list
```

List articles from a specific feed:
```bash
news-app article list --feed-id 1
```

### Reading articles

```bash
news-app article read 1
```

## Development

### AI Summarization

Set your OpenAI API key:
```bash
export OPENAI_API_KEY=your_api_key_here
```

## Development
To run the app directly:

```bash
uv run python main.py
```

## Testing

Install test dependencies:
```bash
uv sync --extra test
```

Run tests:
```bash
uv run pytest
```

## Dependencies

 - feedparser: For parsing RSS feeds
 - click: For creating the CLI interface
 - rich: For beautiful terminal output
 - openai: For AI-powered article summarization
 - requests: For fetching and scraping web articles
 - beautifulsoup4: For parsing HTML content
