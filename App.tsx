import React, { useMemo, useState } from 'react';
import { SafeAreaView, StyleSheet, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';

import { CategoryTabs } from './src/components/CategoryTabs';
import { StoryList } from './src/components/StoryList';
import { getCategoryConfig } from './src/constants/categories';
import { useStories } from './src/hooks/useStories';
import type { StoryCategory } from './src/types/hackerNews';
import { ExpoText, ExpoVStack } from './src/ui/ExpoUI';

export default function App() {
  const [category, setCategory] = useState<StoryCategory>('top');
  const { stories, loading, refreshing, error, refresh, reload } = useStories(category);

  const categoryConfig = useMemo(() => getCategoryConfig(category), [category]);
  const description = categoryConfig.description;
  const subtitle = categoryConfig.label;

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <View style={styles.container}>
        <ExpoVStack spacing={12} style={styles.header}>
          <ExpoText variant="title" weight="bold">
            Hacker News
          </ExpoText>
          <ExpoText variant="body" color="#555">
            Real-time stories sourced from the official Firebase Hacker News API.
          </ExpoText>
          <CategoryTabs selected={category} onSelect={setCategory} />
          <ExpoText variant="caption" color="#888">
            {`Viewing ${subtitle.toLowerCase()} stories`}
          </ExpoText>
        </ExpoVStack>
        <StoryList
          stories={stories}
          loading={loading}
          refreshing={refreshing}
          error={error}
          onRefresh={refresh}
          onRetry={reload}
          description={description}
        />
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  },
  header: {
    paddingHorizontal: 16,
    paddingBottom: 16,
    paddingTop: 12
  }
});
