import React from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

import { ExpoText } from '../ui/ExpoUI';

interface LoadingStateProps {
  label?: string;
}

export function LoadingState({ label = 'Loading stories…' }: LoadingStateProps) {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="small" color="#ff6600" style={styles.indicator} />
      <ExpoText variant="body" color="#666">
        {label}
      </ExpoText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 24
  },
  indicator: {
    marginBottom: 12
  }
});
