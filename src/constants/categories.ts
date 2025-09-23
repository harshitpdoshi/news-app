import type { StoryCategory } from '../types/hackerNews';

export interface StoryCategoryConfig {
  id: StoryCategory;
  label: string;
  endpoint: string;
  description: string;
}

export const STORY_CATEGORIES: StoryCategoryConfig[] = [
  {
    id: 'top',
    label: 'Top',
    endpoint: 'topstories',
    description: 'Most popular stories across Hacker News.'
  },
  {
    id: 'new',
    label: 'New',
    endpoint: 'newstories',
    description: 'Fresh off the press submissions ordered chronologically.'
  },
  {
    id: 'best',
    label: 'Best',
    endpoint: 'beststories',
    description: 'High scoring stories curated by the community.'
  },
  {
    id: 'ask',
    label: 'Ask HN',
    endpoint: 'askstories',
    description: 'Questions and discussions posted by the community.'
  },
  {
    id: 'show',
    label: 'Show HN',
    endpoint: 'showstories',
    description: 'Product and project demos shared by makers.'
  },
  {
    id: 'job',
    label: 'Jobs',
    endpoint: 'jobstories',
    description: 'Latest job postings from the Hacker News community.'
  }
];

export function getCategoryConfig(category: StoryCategory): StoryCategoryConfig {
  const config = STORY_CATEGORIES.find((item) => item.id === category);
  if (!config) {
    throw new Error(`Unknown story category: ${category}`);
  }
  return config;
}
