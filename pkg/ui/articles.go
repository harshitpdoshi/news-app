package ui

import (
	"fmt"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/your-org/news-app/pkg/db"
)

// articleItem wraps a db.Article and feed title to implement list.Item.
type articleItem struct {
	Article   db.Article
	FeedTitle string
}

// Title returns the article title for the list view.
func (a articleItem) Title() string { return a.Article.Title }

// Description shows the feed title.
func (a articleItem) Description() string { return a.FeedTitle }

// FilterValue is used for filtering articles by title.
func (a articleItem) FilterValue() string { return a.Article.Title }

// articleListModel holds state for the article list screen.
type articleListModel struct {
	db   *db.DB
	feed db.Feed
	list list.Model
}

// newArticleListModel creates an article list screen for the given feed.
func newArticleListModel(d *db.DB, feed db.Feed) articleListModel {
	articles, err := d.GetArticlesByFeed(feed.ID, 100)
	if err != nil {
		panic(fmt.Errorf("failed to load articles: %w", err))
	}
	items := make([]list.Item, len(articles))
	for i, art := range articles {
		items[i] = articleItem{Article: art, FeedTitle: feed.Title}
	}
	l := list.New(items, list.NewDefaultDelegate(), 0, 0)
	l.Title = fmt.Sprintf("Articles - %s", feed.Title)
	return articleListModel{db: d, feed: feed, list: l}
}

// Init implements tea.Model.Init.
func (a articleListModel) Init() tea.Cmd { return nil }

// Update handles messages in the article list screen.
func (a articleListModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	m := a
	m.list, cmd = m.list.Update(msg)
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "enter":
			// TODO: switch to article detail view
		case "q", "esc":
			return m, tea.Quit
		}
	}
	return m, cmd
}

// View renders the article list screen.
func (a articleListModel) View() string {
	return a.list.View()
}
