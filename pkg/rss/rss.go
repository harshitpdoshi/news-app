package rss

import (
	"time"

	"github.com/mmcdole/gofeed"
	"github.com/your-org/news-app/pkg/db"
)

// UpdateFeed fetches the RSS feed metadata and new articles for a single feed.
// It updates the feed's title, description, and last_updated timestamp,
// and inserts any new articles. Returns the number of articles added.
func UpdateFeed(d *db.DB, f db.Feed) (int, error) {
	parser := gofeed.NewParser()
	feedData, err := parser.ParseURL(f.URL)
	if err != nil {
		return 0, err
	}
	// Update feed metadata
	now := time.Now().UTC()
	if feedData.Title != "" || feedData.Description != "" {
		_ = d.UpdateFeedMeta(f.ID, feedData.Title, feedData.Description, now)
	}
	// Collect articles
	var articles []db.Article
	for _, item := range feedData.Items {
		var pub *time.Time
		if item.PublishedParsed != nil {
			t := item.PublishedParsed.UTC()
			pub = &t
		}
		articles = append(articles, db.Article{
			FeedID:    f.ID,
			Title:     item.Title,
			Link:      item.Link,
			Summary:   item.Description,
			Published: pub,
			Author:    item.Author.Name,
			Read:      false,
		})
	}
	added, err := d.AddArticles(articles)
	if err != nil {
		return added, err
	}
	// Update last_updated timestamp
	_ = d.UpdateFeedMeta(f.ID, f.Title, f.Description, now)
	return added, nil
}

// UpdateAllFeeds fetches and updates all feeds in the database.
// Returns a map of feed ID to number of articles added for each feed.
func UpdateAllFeeds(d *db.DB) (map[int]int, error) {
	feeds, err := d.GetAllFeeds()
	if err != nil {
		return nil, err
	}
	results := make(map[int]int, len(feeds))
	for _, f := range feeds {
		count, err := UpdateFeed(d, f)
		if err != nil {
			continue
		}
		results[f.ID] = count
	}
	return results, nil
}
