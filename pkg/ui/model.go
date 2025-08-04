package ui

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/your-org/news-app/pkg/db"
)

type screen int

const (
	screenFeeds screen = iota
	screenArticles
	screenDetail
)

// model is the top-level Bubble Tea model that switches between screens.
type model struct {
	db       *db.DB
	state    screen
	feeds    feedListModel
	articles articleListModel
	detail   detailModel
}

// initialModel creates the root model starting on the feeds screen.
func initialModel(d *db.DB) model {
	return model{
		db:    d,
		state: screenFeeds,
		feeds: newFeedListModel(d),
	}
}

// Init is called when the program starts.
func (m model) Init() tea.Cmd {
	return m.feeds.Init()
}

// Update dispatches messages to the current screen's Update method and handles navigation.
func (m model) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	switch m.state {
	case screenFeeds:
		fm, cmd := m.feeds.Update(msg)
		m.feeds = fm.(feedListModel)
		if km, ok := msg.(tea.KeyMsg); ok && km.String() == "enter" {
			selected := m.feeds.list.SelectedItem().(feedItem)
			feed := selected.feed
			m.articles = newArticleListModel(m.db, feed)
			m.state = screenArticles
			return m, m.articles.Init()
		}
		return m, cmd

	case screenArticles:
		am, cmd := m.articles.Update(msg)
		m.articles = am.(articleListModel)
		if km, ok := msg.(tea.KeyMsg); ok {
			switch km.String() {
			case "enter":
				selected := m.articles.list.SelectedItem().(articleItem)
				m.detail = newDetailModel(m.articles.feed, selected.Article)
				m.state = screenDetail
				return m, m.detail.Init()
			case "b":
				m.state = screenFeeds
				return m, m.feeds.Init()
			}
		}
		return m, cmd

	case screenDetail:
		dm, cmd := m.detail.Update(msg)
		m.detail = dm.(detailModel)
		if km, ok := msg.(tea.KeyMsg); ok && km.String() == "b" {
			m.state = screenArticles
			return m, m.articles.Init()
		}
		return m, cmd
	}
	return m, nil
}

// View renders the view of the current screen.
func (m model) View() string {
	switch m.state {
	case screenFeeds:
		return m.feeds.View()
	case screenArticles:
		return m.articles.View()
	case screenDetail:
		return m.detail.View()
	}
	return ""
}
