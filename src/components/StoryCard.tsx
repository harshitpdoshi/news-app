import React, { useCallback } from 'react';
import { Linking, Pressable, StyleSheet, View } from 'react-native';

import type { StorySummary } from '../types/hackerNews';
import { ExpoButton, ExpoHStack, ExpoText, ExpoVStack } from '../ui/ExpoUI';
import { extractHostname, formatRelativeTime } from '../utils/format';

interface StoryCardProps {
  story: StorySummary;
}

const HN_DISCUSSION_URL = 'https://news.ycombinator.com/item?id=';

export function StoryCard({ story }: StoryCardProps) {
  const { title, author, score, commentCount, url, id, time } = story;
  const hostname = extractHostname(url);

  const discussionUrl = `${HN_DISCUSSION_URL}${id}`;

  const handleOpenStory = useCallback(async () => {
    const target = url ?? discussionUrl;
    if (target) {
      try {
        await Linking.openURL(target);
      } catch (error) {
        console.warn('Failed to open link', error);
      }
    }
  }, [discussionUrl, url]);

  const handleOpenDiscussion = useCallback(async () => {
    try {
      await Linking.openURL(discussionUrl);
    } catch (error) {
      console.warn('Failed to open discussion link', error);
    }
  }, [discussionUrl]);

  return (
    <Pressable onPress={handleOpenStory} accessibilityRole="button" accessibilityLabel={title}>
      <View style={styles.card}>
        <ExpoVStack spacing={12}>
          <ExpoVStack spacing={4}>
            {hostname ? (
              <ExpoText variant="caption" color="#ff6600" weight="semibold">
                {hostname}
              </ExpoText>
            ) : null}
            <ExpoText variant="subtitle" weight="semibold">
              {title}
            </ExpoText>
          </ExpoVStack>
          <ExpoHStack spacing={16} style={styles.metaRow} align="leading">
            <ExpoText variant="caption" color="#666">
              {`by ${author}`}
            </ExpoText>
            <ExpoText variant="caption" color="#666">
              {formatRelativeTime(time)}
            </ExpoText>
          </ExpoHStack>
          <ExpoHStack spacing={16} align="leading">
            <ExpoText variant="body" weight="semibold">
              {`${score} points`}
            </ExpoText>
            <ExpoText variant="body" weight="semibold">
              {`${commentCount} comments`}
            </ExpoText>
          </ExpoHStack>
          <ExpoHStack spacing={12}>
            <ExpoButton label="Read" onPress={handleOpenStory} variant="primary" />
            <ExpoButton label="Discuss" onPress={handleOpenDiscussion} variant="plain" />
          </ExpoHStack>
        </ExpoVStack>
      </View>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  card: {
    padding: 20,
    borderRadius: 16,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOpacity: 0.08,
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 12,
    elevation: 2,
    borderWidth: StyleSheet.hairlineWidth,
    borderColor: '#e2e2e2'
  },
  metaRow: {
    flexWrap: 'wrap'
  }
});
