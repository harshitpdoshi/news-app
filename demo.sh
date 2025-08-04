#!/bin/bash

echo "=== News App Demo ==="
echo ""

echo "1. Adding BBC News RSS feed..."
uv run python main.py feed add https://feeds.bbci.co.uk/news/rss.xml
echo ""

echo "2. Listing all feeds..."
uv run python main.py feed list
echo ""

echo "3. Listing unread articles..."
uv run python main.py article list --limit 3
echo ""

echo "4. Reading the first article..."
# Get the first article ID from the list
FIRST_ID=$(uv run python main.py article list --limit 1 | grep "│ [0-9]" | head -1 | awk '{print $2}')
echo "Reading article ID: $FIRST_ID"
uv run python main.py article read $FIRST_ID
echo ""

echo "5. Listing unread articles again (the read article should be gone)..."
uv run python main.py article list --limit 3
echo ""

echo "Demo complete!"