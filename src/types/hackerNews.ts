export type HackerNewsItemType = 'job' | 'story' | 'comment' | 'poll' | 'pollopt';

export interface HackerNewsItem {
  id: number;
  deleted?: boolean;
  type?: HackerNewsItemType;
  by?: string;
  time?: number;
  text?: string;
  dead?: boolean;
  parent?: number;
  poll?: number;
  kids?: number[];
  url?: string;
  score?: number;
  title?: string;
  parts?: number[];
  descendants?: number;
}

export interface StorySummary {
  id: number;
  title: string;
  author: string;
  score: number;
  url?: string;
  commentCount: number;
  time: number;
  type: HackerNewsItemType;
}

export type StoryCategory = 'top' | 'new' | 'best' | 'ask' | 'show' | 'job';
