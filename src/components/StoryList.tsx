import React from 'react';
import { FlatList, ListRenderItem, StyleSheet, View } from 'react-native';

import type { StorySummary } from '../types/hackerNews';
import { ExpoContentUnavailable, ExpoText } from '../ui/ExpoUI';
import { StoryCard } from './StoryCard';
import { LoadingState } from './LoadingState';

interface StoryListProps {
  stories: StorySummary[];
  loading: boolean;
  refreshing: boolean;
  error: Error | null;
  onRefresh: () => void;
  onRetry: () => void;
  description: string;
}

const renderItem: ListRenderItem<StorySummary> = ({ item }) => (
  <View style={styles.cardWrapper}>
    <StoryCard story={item} />
  </View>
);

export function StoryList({
  stories,
  loading,
  refreshing,
  error,
  onRefresh,
  onRetry,
  description
}: StoryListProps) {
  if (error) {
    return (
      <ExpoContentUnavailable
        title="Unable to load stories"
        description={error.message}
        actionLabel="Try again"
        onPressAction={onRetry}
      />
    );
  }

  if (loading && stories.length === 0) {
    return <LoadingState />;
  }

  return (
    <FlatList
      data={stories}
      keyExtractor={(item) => item.id.toString()}
      renderItem={renderItem}
      refreshing={refreshing}
      onRefresh={onRefresh}
      contentContainerStyle={[styles.listContent, stories.length === 0 && styles.emptyState]}
      ListHeaderComponent={
        <View style={styles.descriptionWrapper}>
          <ExpoText variant="body" color="#555">
            {description}
          </ExpoText>
        </View>
      }
      ListFooterComponent={loading ? <LoadingState label="Fetching more stories…" /> : null}
      ItemSeparatorComponent={() => <View style={styles.separator} />}
      ListEmptyComponent={
        !loading ? (
          <ExpoContentUnavailable
            title="No stories yet"
            description="Check back soon for fresh discussions."
            actionLabel="Refresh"
            onPressAction={onRetry}
          />
        ) : undefined
      }
    />
  );
}

const styles = StyleSheet.create({
  listContent: {
    paddingBottom: 40,
    paddingHorizontal: 16
  },
  emptyState: {
    flexGrow: 1,
    justifyContent: 'center'
  },
  separator: {
    height: 16
  },
  cardWrapper: {
    shadowColor: 'transparent'
  },
  descriptionWrapper: {
    marginHorizontal: 4,
    marginBottom: 16
  }
});
