package ui

import (
	"fmt"

	"github.com/charmbracelet/bubbles/list"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/your-org/news-app/pkg/db"
)

// feedItem wraps a db.Feed to implement list.Item.
// feedItem wraps a db.Feed to implement list.Item.
type feedItem struct {
	feed db.Feed
}

// Title returns the feed title for the list view.
func (f feedItem) Title() string { return f.feed.Title }

// Description returns the feed URL for the list view.
func (f feedItem) Description() string { return f.feed.URL }

// FilterValue is used for filtering feeds by title.
func (f feedItem) FilterValue() string { return f.feed.Title }

// feedListModel holds the state for the feed list screen.
type feedListModel struct {
	db   *db.DB
	list list.Model
}

// newFeedListModel creates a feed list screen.
func newFeedListModel(d *db.DB) feedListModel {
	feeds, err := d.GetAllFeeds()
	if err != nil {
		panic(fmt.Errorf("failed to load feeds: %w", err))
	}
	items := make([]list.Item, len(feeds))
	for i, f := range feeds {
		items[i] = feedItem{feed: f}
	}
	l := list.New(items, list.NewDefaultDelegate(), 0, 0)
	l.Title = "Feeds"
	return feedListModel{db: d, list: l}
}

// Init implements tea.Model.Init.
func (f feedListModel) Init() tea.Cmd {
	return nil
}

// Update handles messages in the feed list screen.
func (f feedListModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	m := f
	m.list, cmd = m.list.Update(msg)
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "enter":
			// TODO: switch to article list for selected feed
		case "q", "esc":
			return m, tea.Quit
		}
	}
	return m, cmd
}

// View renders the feed list screen.
func (f feedListModel) View() string {
	return f.list.View()
}
