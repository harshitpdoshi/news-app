# News App - CLI RSS Reader (TUI)

A command-line RSS feed reader built with Go, Bubble Tea, and Glamour.

## Features

- Add and manage RSS feeds
- Fetch and read articles from feeds
- Mark articles as read
- View unread articles
- AI-powered article summarization
- Update feeds to get new articles

## Installation

Requires Go 1.21 or later.

Install the binary:

```bash
go install github.com/your-org/news-app/cmd/news-app@latest
```

## Usage

Run the TUI application:

```bash
news-app
```

Use the arrow keys to navigate feeds and articles, Enter to select, `b` to go back, and `q` to quit.

## Configuration

The database file `feeds.db` is created in the current directory on first run. Add your RSS feeds
directly to the database (e.g. via a separate tool) before launching the TUI.

## License

MIT
