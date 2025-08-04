package ui

import (
	tea "github.com/charmbracelet/bubbletea"
	"github.com/your-org/news-app/pkg/db"
)

// Run starts the Bubble Tea-based TUI application.
func Run() error {
	// Open database
	d, err := db.New("feeds.db")
	if err != nil {
		return err
	}
	defer d.Close()

	// Initialize root model and start Bubble Tea program
	m := initialModel(d)
	p := tea.NewProgram(m)
	return p.Start()
}
