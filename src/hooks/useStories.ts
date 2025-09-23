import { useCallback, useEffect, useMemo, useRef, useState } from 'react';

import { fetchStories } from '../api/hackerNews';
import type { StoryCategory, StorySummary } from '../types/hackerNews';

interface StoriesState {
  stories: StorySummary[];
  loading: boolean;
  refreshing: boolean;
  error: Error | null;
  reload: () => void;
  refresh: () => void;
}

function useAbortController() {
  const controllerRef = useRef<AbortController | null>(null);

  const assign = useCallback((controller: AbortController) => {
    controllerRef.current?.abort();
    controllerRef.current = controller;
  }, []);

  const abort = useCallback(() => {
    controllerRef.current?.abort();
    controllerRef.current = null;
  }, []);

  useEffect(() => abort, [abort]);

  return { assign, abort, controllerRef };
}

export function useStories(category: StoryCategory, limit = 30): StoriesState {
  const [{ stories, loading, refreshing, error }, setState] = useState({
    stories: [] as StorySummary[],
    loading: true,
    refreshing: false,
    error: null as Error | null
  });

  const { assign, abort } = useAbortController();

  const loadStories = useCallback(
    async (mode: 'initial' | 'refresh') => {
      const controller = new AbortController();
      assign(controller);

      setState((prev) => ({
        ...prev,
        loading: mode === 'initial',
        refreshing: mode === 'refresh',
        error: mode === 'initial' ? null : prev.error
      }));

      try {
        const result = await fetchStories(category, {
          limit,
          signal: controller.signal,
          bypassCache: mode === 'refresh'
        });

        if (controller.signal.aborted) {
          return;
        }

        setState({ stories: result, loading: false, refreshing: false, error: null });
      } catch (caughtError) {
        if ((caughtError as Error).name === 'AbortError') {
          return;
        }

        setState((prev) => ({
          ...prev,
          loading: false,
          refreshing: false,
          error: caughtError as Error
        }));
      }
    },
    [assign, category, limit]
  );

  useEffect(() => {
    loadStories('initial');
    return () => {
      abort();
    };
  }, [abort, category, loadStories]);

  const actions = useMemo(
    () => ({
      reload: () => loadStories('initial'),
      refresh: () => loadStories('refresh')
    }),
    [loadStories]
  );

  return { stories, loading, refreshing, error, ...actions };
}
