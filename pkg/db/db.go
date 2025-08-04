package db

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"time"
)

// DB handles SQLite connection and schema.
type DB struct {
	conn *sql.DB
}

// UpdateFeedMeta updates the feed's title, description, and last_updated timestamp.
func (d *DB) UpdateFeedMeta(id int, title, description string, lastUpdated time.Time) error {
	_, err := d.conn.Exec(
		`UPDATE feeds SET title = ?, description = ?, last_updated = ? WHERE id = ?`,
		title, description, lastUpdated.Format(time.RFC3339), id,
	)
	return err
}

// New opens or creates the SQLite database at the given path and initializes the schema.
func New(path string) (*DB, error) {
	conn, err := sql.Open("sqlite3", path)
	if err != nil {
		return nil, err
	}
	d := &DB{conn: conn}
	if err := d.initSchema(); err != nil {
		return nil, err
	}
	return d, nil
}

// Feed represents an RSS feed stored in the database.
type Feed struct {
	ID          int
	URL         string
	Title       string
	Description string
	LastUpdated *time.Time
}

// Article represents a feed article stored in the database.
type Article struct {
	ID        int
	FeedID    int
	Title     string
	Link      string
	Summary   string
	Published *time.Time
	Author    string
	Read      bool
}

// AddFeed inserts a new feed or returns the existing one.
func (d *DB) AddFeed(url, title, description string) (Feed, error) {
	_, err := d.conn.Exec(
		`INSERT OR IGNORE INTO feeds (url, title, description, last_updated) VALUES (?, ?, ?, NULL)`,
		url, title, description,
	)
	if err != nil {
		return Feed{}, err
	}
	return d.GetFeedByURL(url)
}

// GetFeedByURL fetches a feed by its URL.
func (d *DB) GetFeedByURL(url string) (Feed, error) {
	row := d.conn.QueryRow(
		`SELECT id, url, title, description, last_updated FROM feeds WHERE url = ?`, url,
	)
	var f Feed
	var ts sql.NullTime
	if err := row.Scan(&f.ID, &f.URL, &f.Title, &f.Description, &ts); err != nil {
		return Feed{}, err
	}
	if ts.Valid {
		f.LastUpdated = &ts.Time
	}
	return f, nil
}

// GetAllFeeds returns all feeds in the database.
func (d *DB) GetAllFeeds() ([]Feed, error) {
	rows, err := d.conn.Query(`SELECT id, url, title, description, last_updated FROM feeds`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var feeds []Feed
	for rows.Next() {
		var f Feed
		var ts sql.NullTime
		if err := rows.Scan(&f.ID, &f.URL, &f.Title, &f.Description, &ts); err != nil {
			return nil, err
		}
		if ts.Valid {
			f.LastUpdated = &ts.Time
		}
		feeds = append(feeds, f)
	}
	return feeds, rows.Err()
}

// GetFeedByID fetches a feed by its ID.
func (d *DB) GetFeedByID(id int) (Feed, error) {
	row := d.conn.QueryRow(
		`SELECT id, url, title, description, last_updated FROM feeds WHERE id = ?`, id,
	)
	var f Feed
	var ts sql.NullTime
	if err := row.Scan(&f.ID, &f.URL, &f.Title, &f.Description, &ts); err != nil {
		return Feed{}, err
	}
	if ts.Valid {
		f.LastUpdated = &ts.Time
	}
	return f, nil
}

// DeleteFeed removes a feed and its articles.
func (d *DB) DeleteFeed(id int) error {
	if _, err := d.conn.Exec(`DELETE FROM articles WHERE feed_id = ?`, id); err != nil {
		return err
	}
	_, err := d.conn.Exec(`DELETE FROM feeds WHERE id = ?`, id)
	return err
}

// AddArticles inserts multiple articles, ignoring duplicates, and returns the count added.
func (d *DB) AddArticles(articles []Article) (int, error) {
	tx, err := d.conn.Begin()
	if err != nil {
		return 0, err
	}
	stmt, err := tx.Prepare(
		`INSERT OR IGNORE INTO articles (feed_id, title, link, summary, published, author, read) VALUES (?, ?, ?, ?, ?, ?, ?)`,
	)
	if err != nil {
		return 0, err
	}
	defer stmt.Close()
	count := 0
	for _, a := range articles {
		var ts interface{}
		if a.Published != nil {
			ts = a.Published.Format(time.RFC3339)
		}
		res, err := stmt.Exec(a.FeedID, a.Title, a.Link, a.Summary, ts, a.Author, a.Read)
		if err != nil {
			continue
		}
		if n, _ := res.RowsAffected(); n > 0 {
			count++
		}
	}
	tx.Commit()
	return count, nil
}

// GetArticlesByFeed returns articles for a feed, ordered by published desc.
func (d *DB) GetArticlesByFeed(feedID, limit int) ([]Article, error) {
	rows, err := d.conn.Query(
		`SELECT id, feed_id, title, link, summary, published, author, read FROM articles WHERE feed_id = ? ORDER BY published DESC LIMIT ?`,
		feedID, limit,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	return scanArticles(rows)
}

// GetUnreadArticles returns unread articles, ordered by published desc.
func (d *DB) GetUnreadArticles(limit int) ([]Article, error) {
	rows, err := d.conn.Query(
		`SELECT id, feed_id, title, link, summary, published, author, read FROM articles WHERE read = 0 ORDER BY published DESC LIMIT ?`,
		limit,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	return scanArticles(rows)
}

// scanArticles is a helper to read Article rows.
func scanArticles(rows *sql.Rows) ([]Article, error) {
	var list []Article
	for rows.Next() {
		var a Article
		var ts sql.NullTime
		if err := rows.Scan(&a.ID, &a.FeedID, &a.Title, &a.Link, &a.Summary, &ts, &a.Author, &a.Read); err != nil {
			return nil, err
		}
		if ts.Valid {
			a.Published = &ts.Time
		}
		list = append(list, a)
	}
	return list, rows.Err()
}

// MarkArticleAsRead sets the read flag for an article.
func (d *DB) MarkArticleAsRead(articleID int) error {
	_, err := d.conn.Exec(`UPDATE articles SET read = 1 WHERE id = ?`, articleID)
	return err
}

// GetArticleByID fetches a single article by ID.
func (d *DB) GetArticleByID(articleID int) (Article, error) {
	row := d.conn.QueryRow(
		`SELECT id, feed_id, title, link, summary, published, author, read FROM articles WHERE id = ?`, articleID,
	)
	var a Article
	var ts sql.NullTime
	if err := row.Scan(&a.ID, &a.FeedID, &a.Title, &a.Link, &a.Summary, &ts, &a.Author, &a.Read); err != nil {
		return Article{}, err
	}
	if ts.Valid {
		a.Published = &ts.Time
	}
	return a, nil
}

// UpdateFeedLastUpdated sets the last_updated timestamp for a feed.
func (d *DB) UpdateFeedLastUpdated(feedID int, t time.Time) error {
	_, err := d.conn.Exec(`UPDATE feeds SET last_updated = ? WHERE id = ?`, t.Format(time.RFC3339), feedID)
	return err
}

// initSchema creates the feeds and articles tables if they do not exist.
func (d *DB) initSchema() error {
	schema := `
CREATE TABLE IF NOT EXISTS feeds (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   url TEXT UNIQUE NOT NULL,
   title TEXT NOT NULL,
   description TEXT,
   last_updated DATETIME
);

CREATE TABLE IF NOT EXISTS articles (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   feed_id INTEGER NOT NULL REFERENCES feeds(id),
   title TEXT NOT NULL,
   link TEXT NOT NULL UNIQUE,
   summary TEXT,
   published DATETIME,
   author TEXT,
   read BOOLEAN DEFAULT FALSE
);
`
	_, err := d.conn.Exec(schema)
	return err
}

// Close closes the database connection.
func (d *DB) Close() error {
	return d.conn.Close()
}
