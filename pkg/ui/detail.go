package ui

import (
	"fmt"

	"github.com/charmbracelet/bubbles/spinner"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/glamour"
	"github.com/your-org/news-app/pkg/db"
)

// detailModel holds state for the article detail screen, including AI summary loading.
type detailModel struct {
	feed    db.Feed
	article db.Article
	summary string
	spinner spinner.Model
	loading bool
}

// aiMsg carries the AI-generated summary.
type aiMsg string

// newDetailModel creates a detail view for an article.
func newDetailModel(feed db.Feed, article db.Article) detailModel {
	sp := spinner.New()
	sp.Spinner = spinner.Dot
	return detailModel{
		feed:    feed,
		article: article,
		spinner: sp,
		loading: true,
	}
}

// Init starts the spinner and kicks off AI summary fetch.
func (m detailModel) Init() tea.Cmd {
	return tea.Batch(m.spinner.Tick, fetchAISummary(m.article.Link))
}

// fetchAISummary is a placeholder for calling an AI summarization API.
func fetchAISummary(link string) tea.Cmd {
	return func() tea.Msg {
		// TODO: integrate OpenAI client to summarize article link
		return aiMsg("[AI summary placeholder]")
	}
}

// Update handles spinner ticks, AI summary, and key events.
func (m detailModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmd tea.Cmd
	switch msg := msg.(type) {
	case spinner.TickMsg:
		m.spinner, cmd = m.spinner.Update(msg)
		return m, cmd
	case aiMsg:
		m.summary = string(msg)
		m.loading = false
		return m, nil
	case tea.KeyMsg:
		switch msg.String() {
		case "b":
			// TODO: navigate back to article list
		case "q", "esc":
			return m, tea.Quit
		}
	}
	return m, nil
}

// View renders the article detail screen.
func (m detailModel) View() string {
	view := fmt.Sprintf("%s\n(%s)\n\n", m.article.Title, m.feed.Title)
	if rendered, err := glamour.Render(m.article.Summary, "dark"); err == nil {
		view += rendered + "\n\n"
	} else {
		view += m.article.Summary + "\n\n"
	}
	if m.loading {
		view += m.spinner.View() + " Generating AI summary..."
	} else {
		view += "AI Summary:\n"
		if rendered, err := glamour.Render(m.summary, "dark"); err == nil {
			view += rendered
		} else {
			view += m.summary
		}
	}
	view += "\n\n(press b to go back, q to quit)"
	return view
}
