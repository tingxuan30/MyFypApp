import React from 'react';
import {
  Tabs,
  TabList,
  TabTrigger,
  TabSlot,
  TabTriggerSlotProps,
  TabListProps,
} from 'expo-router/ui';
import { SymbolView } from 'expo-symbols';
import {
  Pressable,
  View,
  StyleSheet,
  useColorScheme,
} from 'react-native';

import { Colors, MaxContentWidth, Spacing } from '@/constants/theme';
import { ThemedText } from './themed-text';
import { ThemedView } from './themed-view';

const tabs = [
  { name: 'home', title: 'Home', href: '/', icon: { ios: 'house.fill', android: 'home', web: 'home' } },
  { name: 'vegetables', title: 'Vegetables', href: '/vegetables', icon: { ios: 'leaf.fill', android: 'eco', web: 'eco' } },
  { name: 'scan', title: 'Scan', href: '/scan', icon: { ios: 'viewfinder', android: 'qr_code_scanner', web: 'qr_code_scanner' } },
  { name: 'forecast', title: 'Forecast', href: '/forecast', icon: { ios: 'chart.line.uptrend.xyaxis', android: 'trending_up', web: 'trending_up' } },
  { name: 'ai-assistant', title: 'AI Assistant', href: '/ai-assistant', icon: { ios: 'sparkles', android: 'auto_awesome', web: 'auto_awesome' } },
] as const;

type TabIcon = { ios: string; android: string; web: string };
type TabButtonProps = TabTriggerSlotProps & {
  icon: TabIcon;
  children: React.ReactNode;
};

export default function AppTabs() {
  return (
    <Tabs>
      <TabSlot style={styles.tabSlot} />
      <TabList asChild>
        <CustomTabList>
          {tabs.map((tab) => (
            <TabTrigger key={tab.name} name={tab.name} href={tab.href} asChild>
              <TabButton icon={tab.icon}>{tab.title}</TabButton>
            </TabTrigger>
          ))}
        </CustomTabList>
      </TabList>
    </Tabs>
  );
}

export function TabButton({ children, icon, isFocused, ...props }: TabButtonProps) {
  const scheme = useColorScheme();
  const colors = Colors[scheme === 'dark' ? 'dark' : 'light'];

  return (
    <Pressable
      {...props}
      accessibilityRole="tab"
      style={({ pressed }) => [styles.tabButton, pressed && styles.pressed]}
    >
      <SymbolView
        name={icon}
        tintColor={isFocused ? '#087653' : colors.text}
        size={21}
      />
      <ThemedText
        type="small"
        numberOfLines={1}
        style={[styles.tabLabel, isFocused && styles.activeLabel]}
      >
        {children}
      </ThemedText>
    </Pressable>
  );
}

export function CustomTabList(props: TabListProps) {
  return (
    <View {...props} style={styles.tabListContainer}>
      <ThemedView type="backgroundElement" style={styles.innerContainer}>
        {props.children}
      </ThemedView>
    </View>
  );
}

const styles = StyleSheet.create({
  tabSlot: { flex: 1 },
  tabListContainer: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    alignItems: 'center',
    paddingHorizontal: Spacing.two,
    paddingTop: Spacing.two,
    paddingBottom: Spacing.two,
  },
  innerContainer: {
    width: '100%',
    maxWidth: MaxContentWidth,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-around',
    paddingVertical: Spacing.two,
    paddingHorizontal: Spacing.one,
    borderRadius: Spacing.four,
    gap: 0,
  },
  tabButton: {
    flex: 1,
    minWidth: 0,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 5,
    paddingVertical: Spacing.two,
    paddingHorizontal: 2,
  },
  tabLabel: { fontSize: 10, textAlign: 'center' },
  activeLabel: { color: '#087653', fontWeight: '700' },
  pressed: { opacity: 0.65 },
});
