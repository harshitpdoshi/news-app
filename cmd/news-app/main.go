package main

import (
	"log"

	"github.com/your-org/news-app/pkg/ui"
)

// main is the entrypoint for the TUI application.
func main() {
	if err := ui.Run(); err != nil {
		log.Fatal(err)
	}
}
