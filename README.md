# Hacker News Expo App

A production-ready Hacker News client built with Expo SDK 54 and the experimental Expo UI component library. The app surfaces top, new, best, Ask HN, Show HN, and job stories using the official Firebase-powered Hacker News API.

## Getting started

```bash
npm install
npm run start
```

Scan the QR code with the Expo Go app or run the project in an iOS Simulator, Android Emulator, or the web browser from the Expo CLI dashboard.

## Tech highlights

- **Expo SDK 54.0.9** with TypeScript strict mode enabled for confident builds.
- **Expo UI** (`@expo/ui`) components adapted across iOS SwiftUI and Android Jetpack Compose with graceful web fallbacks.
- **Resilient data layer** backed by the Firebase Hacker News API with caching, abortable fetches, and retry handling.
- **Human-friendly UX** featuring responsive category filters, contextual empty states, and deep linking into original posts or Hacker News discussions.

## Project structure

```
src/
  api/             # API client helpers
  components/      # Reusable presentation components
  constants/       # Static configuration such as category metadata
  hooks/           # Custom React hooks
  types/           # Shared TypeScript types
  ui/              # Cross-platform Expo UI adapters
  utils/           # Formatting helpers
```

## API reference

All data is sourced from the public Hacker News API documented at https://github.com/HackerNews/API and mirrored in Firebase.
