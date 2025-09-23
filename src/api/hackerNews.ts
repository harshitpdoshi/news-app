import { getCategoryConfig } from '../constants/categories';
import type { HackerNewsItem, StoryCategory, StorySummary } from '../types/hackerNews';

const API_BASE_URL = 'https://hacker-news.firebaseio.com/v0';
const JSON_SUFFIX = '.json';
const DEFAULT_STORY_LIMIT = 30;

const storyCache = new Map<number, StorySummary>();
const idCache = new Map<StoryCategory, number[]>();

interface FetchOptions {
  signal?: AbortSignal;
  limit?: number;
  bypassCache?: boolean;
}

async function fetchJson<T>(path: string, signal?: AbortSignal): Promise<T> {
  const response = await fetch(`${API_BASE_URL}/${path}${path.endsWith(JSON_SUFFIX) ? '' : JSON_SUFFIX}`, {
    signal,
    headers: {
      Accept: 'application/json'
    }
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${response.statusText}`);
  }

  return (await response.json()) as T;
}

async function fetchItem(id: number, signal?: AbortSignal): Promise<HackerNewsItem> {
  return fetchJson<HackerNewsItem>(`item/${id}.json`, signal);
}

function toStorySummary(item: HackerNewsItem): StorySummary | null {
  if (!item || !item.id) {
    return null;
  }

  const title = item.title ?? 'Untitled';
  const author = item.by ?? 'unknown';
  const type = item.type ?? 'story';

  if (item.dead || item.deleted) {
    return null;
  }

  return {
    id: item.id,
    title,
    author,
    score: item.score ?? 0,
    url: item.url,
    commentCount: item.descendants ?? item.kids?.length ?? 0,
    time: item.time ?? 0,
    type
  };
}

async function hydrateStory(id: number, signal?: AbortSignal): Promise<StorySummary | null> {
  const cached = storyCache.get(id);
  if (cached) {
    return cached;
  }

  const item = await fetchItem(id, signal);
  const summary = toStorySummary(item);

  if (summary) {
    storyCache.set(id, summary);
  }

  return summary;
}

export async function fetchStoryIds(
  category: StoryCategory,
  { signal, bypassCache }: Pick<FetchOptions, 'signal' | 'bypassCache'> = {}
): Promise<number[]> {
  if (!bypassCache && idCache.has(category)) {
    return idCache.get(category)!;
  }

  const config = getCategoryConfig(category);
  const ids = await fetchJson<number[]>(`${config.endpoint}.json`, signal);

  idCache.set(category, ids);
  return ids;
}

async function sequentialAll<T>(
  items: readonly number[],
  limit: number,
  mapper: (id: number) => Promise<T | null>
): Promise<T[]> {
  const result: T[] = [];
  for (const id of items) {
    if (result.length >= limit) {
      break;
    }
    const mapped = await mapper(id);
    if (mapped) {
      result.push(mapped);
    }
  }
  return result;
}

export async function fetchStories(
  category: StoryCategory,
  { signal, limit = DEFAULT_STORY_LIMIT, bypassCache = false }: FetchOptions = {}
): Promise<StorySummary[]> {
  const ids = await fetchStoryIds(category, { signal, bypassCache });

  const summaries = await sequentialAll(ids, limit, async (id) => hydrateStory(id, signal));

  return summaries;
}

export function clearStoryCache() {
  storyCache.clear();
}

export function clearCategoryCache(category?: StoryCategory) {
  if (category) {
    idCache.delete(category);
    return;
  }
  idCache.clear();
}
