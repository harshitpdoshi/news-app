import React from 'react';
import { ScrollView, StyleSheet, View } from 'react-native';

import { STORY_CATEGORIES } from '../constants/categories';
import type { StoryCategory } from '../types/hackerNews';
import { ExpoButton, ExpoHStack, ExpoText } from '../ui/ExpoUI';

interface CategoryTabsProps {
  selected: StoryCategory;
  onSelect: (category: StoryCategory) => void;
}

export function CategoryTabs({ selected, onSelect }: CategoryTabsProps) {
  return (
    <View style={styles.container}>
      <View style={styles.headingWrapper}>
        <ExpoText variant="subtitle" weight="semibold">
          Browse stories
        </ExpoText>
      </View>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.scrollContent}
      >
        <ExpoHStack spacing={12}>
          {STORY_CATEGORIES.map((category) => {
            const isActive = category.id === selected;
            return (
              <ExpoButton
                key={category.id}
                label={category.label}
                variant={isActive ? 'primary' : 'subtle'}
                onPress={() => onSelect(category.id)}
              />
            );
          })}
        </ExpoHStack>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingBottom: 16
  },
  headingWrapper: {
    marginBottom: 8
  },
  scrollContent: {
    paddingRight: 8
  }
});
