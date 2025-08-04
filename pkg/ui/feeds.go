package ui

import (
	"fmt"

	"github.com/charmbracelet/bubbles/list"
	"github.com/charmbracelet/bubbles/textinput"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/your-org/news-app/pkg/db"
	"github.com/your-org/news-app/pkg/rss"
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
	db     *db.DB
	list   list.Model
	adding bool
	input  textinput.Model
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
	ti := textinput.New()
	ti.Placeholder = "Enter RSS URL"
	ti.Focus()
	ti.CharLimit = 256
	ti.Width = 40
	return feedListModel{db: d, list: l, adding: false, input: ti}
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
	if f.adding {
		var cmd tea.Cmd
		f.input, cmd = f.input.Update(msg)
		switch msg := msg.(type) {
		case tea.KeyMsg:
			switch msg.String() {
			case "enter":
				url := f.input.Value()
				if _, err := f.db.AddFeed(url, url, ""); err == nil {
					rss.UpdateFeed(f.db, db.Feed{URL: url})
				}
				return newFeedListModel(f.db), nil
			case "esc":
				f.adding = false
				return newFeedListModel(f.db), nil
			}
		}
		return f, cmd
	}

	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.String() {
		case "enter":
			// switch to article list for selected feed
		case "a":
			f.adding = true
			return f, nil
		case "d":
			if itm, ok := f.list.SelectedItem().(feedItem); ok {
				_ = f.db.DeleteFeed(itm.feed.ID)
				return newFeedListModel(f.db), nil
			}
		case "u":
			if itm, ok := f.list.SelectedItem().(feedItem); ok {
				rss.UpdateFeed(f.db, itm.feed)
				return newFeedListModel(f.db), nil
			}
		case "r":
			rss.UpdateAllFeeds(f.db)
			return newFeedListModel(f.db), nil
		case "q", "esc":
			return f, tea.Quit
		}
	}
	return f, cmd
}

// View renders the feed list screen.
func (f feedListModel) View() string {
	if f.adding {
		return fmt.Sprintf("Add new feed (esc to cancel):\n%s", f.input.View())
	}
	return f.list.View()
}
