import React, { Children } from 'react';
import {
  Platform,
  StyleProp,
  StyleSheet,
  Text as RNText,
  TextStyle,
  View,
  ViewStyle
} from 'react-native';

import {
  Button as SwiftButton,
  ContentUnavailableView,
  HStack as SwiftHStack,
  Spacer as SwiftSpacer,
  Text as SwiftText,
  VStack as SwiftVStack
} from '@expo/ui/swift-ui';
import { Button as ComposeButton } from '@expo/ui/jetpack-compose';
import {
  Column as ComposeColumn,
  Container as ComposeContainer,
  Row as ComposeRow,
  Text as ComposeText
} from '@expo/ui/jetpack-compose-primitives';

type TextVariant = 'title' | 'subtitle' | 'body' | 'caption';

type TextWeight = 'regular' | 'medium' | 'semibold' | 'bold';

const isIOS = Platform.OS === 'ios';
const isAndroid = Platform.OS === 'android';

const TEXT_SIZE_MAP: Record<TextVariant, number> = {
  title: 22,
  subtitle: 16,
  body: 14,
  caption: 12
};

const IOS_WEIGHT_MAP: Record<TextWeight, Parameters<typeof SwiftText>[0]['weight']> = {
  regular: 'regular',
  medium: 'medium',
  semibold: 'semibold',
  bold: 'bold'
};

const ANDROID_WEIGHT_MAP: Record<TextWeight, Parameters<typeof ComposeText>[0]['fontWeight']> = {
  regular: '400',
  medium: '500',
  semibold: '600',
  bold: '700'
};

export interface ExpoTextProps {
  children: string;
  variant?: TextVariant;
  weight?: TextWeight;
  color?: string;
  numberOfLines?: number;
  style?: StyleProp<TextStyle>;
}

export function ExpoText({
  children,
  variant = 'body',
  weight = 'regular',
  color,
  numberOfLines,
  style
}: ExpoTextProps) {
  const size = TEXT_SIZE_MAP[variant];

  if (isIOS) {
    return (
      <SwiftText size={size} weight={IOS_WEIGHT_MAP[weight]} color={color} lineLimit={numberOfLines}>
        {children}
      </SwiftText>
    );
  }

  if (isAndroid) {
    return (
      <ComposeText fontSize={size} fontWeight={ANDROID_WEIGHT_MAP[weight]} color={color}>
        {children}
      </ComposeText>
    );
  }

  return (
    <RNText numberOfLines={numberOfLines} style={[{ fontSize: size, color }, styles.webText, style]}>
      {children}
    </RNText>
  );
}

export interface ExpoButtonProps {
  label: string;
  onPress?: () => void;
  variant?: 'primary' | 'subtle' | 'plain';
  disabled?: boolean;
}

export function ExpoButton({ label, onPress, variant = 'primary', disabled }: ExpoButtonProps) {
  if (isIOS) {
    const iosVariant: Parameters<typeof SwiftButton>[0]['variant'] =
      variant === 'plain' ? 'borderless' : variant === 'subtle' ? 'bordered' : 'borderedProminent';

    return (
      <SwiftButton onPress={onPress} variant={iosVariant} disabled={disabled}>
        {label}
      </SwiftButton>
    );
  }

  if (isAndroid) {
    const androidVariant: Parameters<typeof ComposeButton>[0]['variant'] =
      variant === 'plain' ? 'borderless' : variant === 'subtle' ? 'outlined' : 'elevated';

    return (
      <ComposeButton onPress={onPress} variant={androidVariant} disabled={disabled}>
        {label}
      </ComposeButton>
    );
  }

  return (
    <View style={styles.webButtonContainer}>
      <RNText onPress={disabled ? undefined : onPress} style={[styles.webButton, disabled && styles.webButtonDisabled]}>
        {label}
      </RNText>
    </View>
  );
}

export interface ExpoStackProps {
  spacing?: number;
  style?: StyleProp<ViewStyle>;
  children: React.ReactNode;
  align?: 'leading' | 'center' | 'trailing';
}

export function ExpoVStack({ spacing = 12, style, children, align = 'leading' }: ExpoStackProps) {
  if (isIOS) {
    const content = (
      <SwiftVStack spacing={spacing} alignment={align}>
        {children}
      </SwiftVStack>
    );
    return style ? <View style={style}>{content}</View> : content;
  }

  if (isAndroid) {
    const childArray = Children.toArray(children);
    return (
      <ComposeContainer style={style}>
        <ComposeColumn horizontalAlignment={align === 'center' ? 'center' : align === 'trailing' ? 'end' : 'start'}>
          {childArray.map((child, index) => (
            <View key={index} style={index === 0 ? undefined : { marginTop: spacing }}>
              {child}
            </View>
          ))}
        </ComposeColumn>
      </ComposeContainer>
    );
  }

  return <View style={[styles.webStack, style, { gap: spacing }]}>{children}</View>;
}

export function ExpoHStack({ spacing = 12, style, children, align = 'center' }: ExpoStackProps) {
  if (isIOS) {
    const iosAlignment: Parameters<typeof SwiftHStack>[0]['alignment'] =
      align === 'center' ? 'center' : align === 'trailing' ? 'bottom' : 'top';
    const content = (
      <SwiftHStack spacing={spacing} alignment={iosAlignment}>
        {children}
      </SwiftHStack>
    );
    return style ? <View style={style}>{content}</View> : content;
  }

  if (isAndroid) {
    const childArray = Children.toArray(children);
    return (
      <ComposeContainer style={style}>
        <ComposeRow verticalAlignment={align === 'leading' ? 'top' : align === 'trailing' ? 'bottom' : 'center'}>
          {childArray.map((child, index) => (
            <View key={index} style={index === 0 ? undefined : { marginLeft: spacing }}>
              {child}
            </View>
          ))}
        </ComposeRow>
      </ComposeContainer>
    );
  }

  return (
    <View style={[styles.webRow, style]}>
      {Children.map(children, (child, index) => (
        <View key={index} style={index === 0 ? undefined : { marginLeft: spacing }}>
          {child}
        </View>
      ))}
    </View>
  );
}

export interface ExpoSpacerProps {
  size?: number;
}

export function ExpoSpacer({ size = 12 }: ExpoSpacerProps) {
  if (isIOS) {
    return <SwiftSpacer minLength={size} />;
  }

  return <View style={{ height: size, width: size }} />;
}

export interface ExpoContentUnavailableProps {
  title: string;
  description?: string;
  actionLabel?: string;
  onPressAction?: () => void;
}

export function ExpoContentUnavailable({
  title,
  description,
  actionLabel,
  onPressAction
}: ExpoContentUnavailableProps) {
  if (isIOS) {
    return (
      <View style={styles.iosUnavailableWrapper}>
        <ContentUnavailableView title={title} description={description} />
        {actionLabel ? (
          <View style={styles.iosUnavailableAction}>
            <ExpoButton label={actionLabel} onPress={onPressAction} variant="primary" />
          </View>
        ) : null}
      </View>
    );
  }

  return (
    <View style={styles.webUnavailableContainer}>
      <ExpoText variant="title" weight="semibold">
        {title}
      </ExpoText>
      {description ? (
        <ExpoText variant="body" style={styles.webUnavailableDescription}>
          {description}
        </ExpoText>
      ) : null}
      {actionLabel ? (
        <ExpoButton label={actionLabel} onPress={onPressAction} variant="primary" />
      ) : null}
    </View>
  );
}

const styles = StyleSheet.create({
  webText: {
    fontFamily: 'System'
  },
  webButtonContainer: {
    borderRadius: 999,
    overflow: 'hidden'
  },
  webButton: {
    paddingVertical: 8,
    paddingHorizontal: 16,
    backgroundColor: '#ff6600',
    color: '#fff',
    textAlign: 'center',
    fontWeight: '600'
  },
  webButtonDisabled: {
    opacity: 0.5
  },
  webStack: {
    display: 'flex',
    flexDirection: 'column'
  },
  webRow: {
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'center'
  },
  webUnavailableContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
    gap: 12
  },
  webUnavailableDescription: {
    textAlign: 'center'
  },
  iosUnavailableWrapper: {
    alignItems: 'center',
    gap: 16
  },
  iosUnavailableAction: {
    width: '100%',
    maxWidth: 240
  }
});
