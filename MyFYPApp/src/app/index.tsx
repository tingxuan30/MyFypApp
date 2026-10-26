
import React, { useMemo, useState } from 'react';
import {
  Alert,
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

type Vegetable = {
  name: string;
  emoji: string;
  price: number;
  change: number;
};

const vegetables: Vegetable[] = [
  { name: 'Tomato', emoji: '🍅', price: 4.8, change: -6.3 },
  { name: 'Kangkung', emoji: '🥬', price: 3.2, change: 4.1 },
  { name: 'Cabbage', emoji: '🥬', price: 2.5, change: -2.8 },
  { name: 'Carrot', emoji: '🥕', price: 3.8, change: 3.5 },
];

const green = '#087653';
const dark = '#173C32';
const muted = '#7B8D86';
const bg = '#F5F8F5';

export default function HomeScreen() {
  const [search, setSearch] = useState('');
  const [activeTab, setActiveTab] = useState('Home');

  const filteredVegetables = useMemo(
    () =>
      vegetables.filter((item) =>
        item.name.toLowerCase().includes(search.toLowerCase())
      ),
    [search]
  );

  const handleScan = () => {
    Alert.alert(
      'Scan Vegetable',
      'Camera recognition will be connected in a later development phase.'
    );
  };

  const handleForecast = (name = 'Tomato') => {
    Alert.alert(
      `${name} Price Forecast`,
      'Forecasting will be connected to the historical price dataset and prediction model in a later phase.'
    );
  };

  const handleAI = () => {
    Alert.alert(
      'AI Assistant',
      'Ask questions about vegetable prices, market trends and possible price changes. AI integration will be added later.'
    );
  };

  const handleTab = (tab: string) => {
    setActiveTab(tab);

    if (tab === 'Scan') {
      handleScan();
    } else if (tab === 'Forecast') {
      handleForecast();
    } else if (tab === 'AI Assistant') {
      handleAI();
    }
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={bg} />

      <ScrollView
        showsVerticalScrollIndicator={false}
        contentContainerStyle={styles.content}
      >
        {/* Header */}
        <View style={styles.header}>
          <View style={styles.brandIcon}>
            <Text style={styles.brandEmoji}>🌿</Text>
          </View>

          <View style={styles.brandText}>
            <Text style={styles.brandName}>VegPrice MY</Text>
            <Text style={styles.brandSubtitle}>
              Malaysian Vegetables Analytics
            </Text>
          </View>

          <TouchableOpacity
            style={styles.profileButton}
            onPress={() =>
              Alert.alert('Profile', 'User profile can be added later.')
            }
          >
            <Text style={styles.profileEmoji}>👤</Text>
          </TouchableOpacity>
        </View>

        {/* Welcome banner */}
        <View style={styles.hero}>
          <Text style={styles.heroEyebrow}>YOUR SMART MARKET GUIDE</Text>
          <Text style={styles.heroTitle}>Know your prices.</Text>
          <Text style={styles.heroTitle}>Shop smarter.</Text>
          <Text style={styles.heroDescription}>
            Explore Malaysian vegetable prices, discover trends and
            understand possible future price changes.
          </Text>

          <TouchableOpacity style={styles.scanButton} onPress={handleScan}>
            <Text style={styles.scanButtonText}>
              📷  Scan a Vegetable
            </Text>
          </TouchableOpacity>

          <View style={styles.searchBox}>
            <Text style={styles.searchIcon}>⌕</Text>
            <TextInput
              style={styles.searchInput}
              placeholder="Search vegetables..."
              placeholderTextColor="#91A19A"
              value={search}
              onChangeText={setSearch}
              autoCapitalize="none"
            />
            {search.length > 0 && (
              <TouchableOpacity onPress={() => setSearch('')}>
                <Text style={styles.clearText}>✕</Text>
              </TouchableOpacity>
            )}
          </View>
        </View>

        {/* Market overview */}
        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionTitle}>Market Overview</Text>
            <Text style={styles.sectionSubtitle}>
              Sample prices · RM per kg
            </Text>
          </View>
          <Text style={styles.liveLabel}>DEMO DATA</Text>
        </View>

        <View style={styles.statsRow}>
          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Vegetables</Text>
            <Text style={styles.statValue}>04</Text>
            <Text style={styles.statFoot}>In this demo</Text>
          </View>

          <View style={styles.statCard}>
            <Text style={styles.statLabel}>Average price</Text>
            <Text style={styles.statValue}>RM 3.58</Text>
            <Text style={styles.statFoot}>Per kilogram</Text>
          </View>
        </View>

        {/* Vegetable list */}
        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionTitle}>Vegetable Prices</Text>
            <Text style={styles.sectionSubtitle}>
              Compare recent price movements
            </Text>
          </View>
        </View>

        {filteredVegetables.length === 0 ? (
          <View style={styles.emptyBox}>
            <Text style={styles.emptyText}>
              No vegetables found. Try another name.
            </Text>
          </View>
        ) : (
          filteredVegetables.map((item) => (
            <TouchableOpacity
              key={item.name}
              style={styles.vegetableCard}
              onPress={() =>
                Alert.alert(
                  item.name,
                  `Sample price: RM ${item.price.toFixed(2)}/kg\n` +
                    `Change vs last week: ${item.change > 0 ? '+' : ''}${item.change}%`,
                  [
                    { text: 'Close', style: 'cancel' },
                    {
                      text: 'View Forecast',
                      onPress: () => handleForecast(item.name),
                    },
                  ]
                )
              }
            >
              <View style={styles.vegetableEmojiBox}>
                <Text style={styles.vegetableEmoji}>{item.emoji}</Text>
              </View>

              <View style={styles.vegetableInfo}>
                <Text style={styles.vegetableName}>{item.name}</Text>
                <Text style={styles.vegetablePrice}>
                  RM {item.price.toFixed(2)}
                  <Text style={styles.perKg}> / kg</Text>
                </Text>
                <Text style={styles.vegetableHint}>Tap to explore</Text>
              </View>

              <View style={styles.changeBox}>
                <Text
                  style={[
                    styles.changeValue,
                    { color: item.change <= 0 ? green : '#D65A4A' },
                  ]}
                >
                  {item.change <= 0 ? '↓ ' : '↑ '}
                  {Math.abs(item.change).toFixed(1)}%
                </Text>
                <Text style={styles.changeCaption}>vs last week</Text>
              </View>
            </TouchableOpacity>
          ))
        )}

        {/* AI insight */}
        <View style={styles.insightCard}>
          <View style={styles.insightIcon}>
            <Text style={styles.insightEmoji}>✦</Text>
          </View>
          <View style={styles.insightContent}>
            <Text style={styles.insightTitle}>AI Market Insights</Text>
            <Text style={styles.insightText}>
              Discover price movements and possible market patterns using
              historical data.
            </Text>
            <TouchableOpacity onPress={handleAI}>
              <Text style={styles.insightLink}>Explore insights  →</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Forecast card */}
        <View style={styles.forecastCard}>
          <View style={styles.forecastTop}>
            <View>
              <Text style={styles.forecastEyebrow}>PRICE FORECAST</Text>
              <Text style={styles.forecastTitle}>
                Plan your next purchase
              </Text>
            </View>
            <Text style={styles.forecastEmoji}>📈</Text>
          </View>

          <Text style={styles.forecastDescription}>
            Check historical prices and estimated future trends before
            deciding when to buy.
          </Text>

          <TouchableOpacity
            style={styles.forecastButton}
            onPress={() => handleForecast()}
          >
            <Text style={styles.forecastButtonText}>
              Explore Forecast  →
            </Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.disclaimer}>
          FYP prototype · Sample data only. Prices and forecasts are not
          real-time market information.
        </Text>
      </ScrollView>

      {/* Bottom navigation */}
      <View style={styles.bottomNav}>
        {[
          { label: 'Home', icon: '⌂' },
          { label: 'Scan', icon: '▣' },
          { label: 'Forecast', icon: '▥' },
          { label: 'AI Assistant', icon: '✧' },
        ].map((tab) => (
          <TouchableOpacity
            key={tab.label}
            style={styles.navItem}
            onPress={() => handleTab(tab.label)}
          >
            <Text
              style={[
                styles.navIcon,
                activeTab === tab.label && styles.navActive,
              ]}
            >
              {tab.icon}
            </Text>
            <Text
              style={[
                styles.navLabel,
                activeTab === tab.label && styles.navActive,
              ]}
            >
              {tab.label}
            </Text>
          </TouchableOpacity>
        ))}
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: bg,
  },
  content: {
    paddingHorizontal: 20,
    paddingTop: 12,
    paddingBottom: 24,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 22,
  },
  brandIcon: {
    width: 46,
    height: 46,
    borderRadius: 15,
    backgroundColor: '#E0F1E6',
    alignItems: 'center',
    justifyContent: 'center',
  },
  brandEmoji: {
    fontSize: 27,
  },
  brandText: {
    flex: 1,
    marginLeft: 11,
  },
  brandName: {
    fontSize: 21,
    fontWeight: '800',
    color: dark,
  },
  brandSubtitle: {
    fontSize: 11,
    color: muted,
    marginTop: 3,
  },
  profileButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#E4EEE7',
    alignItems: 'center',
    justifyContent: 'center',
  },
  profileEmoji: {
    fontSize: 20,
  },
  hero: {
    backgroundColor: '#E1F2E8',
    borderRadius: 24,
    padding: 20,
    marginBottom: 28,
    overflow: 'hidden',
  },
  heroEyebrow: {
    color: green,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1.2,
    marginBottom: 12,
  },
  heroTitle: {
    color: dark,
    fontSize: 27,
    fontWeight: '800',
    lineHeight: 33,
  },
  heroDescription: {
    color: '#57766A',
    fontSize: 13,
    lineHeight: 20,
    marginTop: 10,
    marginBottom: 18,
  },
  scanButton: {
    backgroundColor: green,
    borderRadius: 14,
    paddingVertical: 14,
    alignItems: 'center',
    marginBottom: 12,
  },
  scanButtonText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '700',
  },
  searchBox: {
    minHeight: 48,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 13,
    paddingHorizontal: 13,
  },
  searchIcon: {
    color: muted,
    fontSize: 25,
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    color: dark,
    fontSize: 13,
    paddingVertical: 10,
  },
  clearText: {
    color: muted,
    padding: 5,
  },
  sectionHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 14,
  },
  sectionTitle: {
    color: dark,
    fontSize: 19,
    fontWeight: '800',
  },
  sectionSubtitle: {
    color: muted,
    fontSize: 12,
    marginTop: 5,
  },
  liveLabel: {
    color: green,
    backgroundColor: '#E2F1E6',
    paddingHorizontal: 9,
    paddingVertical: 6,
    borderRadius: 8,
    fontSize: 9,
    fontWeight: '800',
  },
  statsRow: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 28,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#FFFFFF',
    padding: 16,
    borderRadius: 17,
    borderWidth: 1,
    borderColor: '#E8EFE9',
  },
  statLabel: {
    color: muted,
    fontSize: 11,
  },
  statValue: {
    color: dark,
    fontSize: 21,
    fontWeight: '800',
    marginTop: 9,
  },
  statFoot: {
    color: green,
    fontSize: 10,
    marginTop: 5,
  },
  vegetableCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFFFFF',
    borderRadius: 17,
    borderWidth: 1,
    borderColor: '#E8EFE9',
    padding: 12,
    marginBottom: 10,
  },
  vegetableEmojiBox: {
    width: 53,
    height: 53,
    borderRadius: 15,
    backgroundColor: '#F0F6EF',
    alignItems: 'center',
    justifyContent: 'center',
  },
  vegetableEmoji: {
    fontSize: 28,
  },
  vegetableInfo: {
    flex: 1,
    marginLeft: 12,
  },
  vegetableName: {
    color: dark,
    fontSize: 14,
    fontWeight: '700',
  },
  vegetablePrice: {
    color: dark,
    fontSize: 15,
    fontWeight: '800',
    marginTop: 4,
  },
  perKg: {
    color: muted,
    fontSize: 11,
    fontWeight: '400',
  },
  vegetableHint: {
    color: muted,
    fontSize: 10,
    marginTop: 4,
  },
  changeBox: {
    alignItems: 'flex-end',
    marginLeft: 5,
  },
  changeValue: {
    fontSize: 13,
    fontWeight: '800',
  },
  changeCaption: {
    color: muted,
    fontSize: 9,
    marginTop: 5,
  },
  emptyBox: {
    padding: 24,
    backgroundColor: '#FFFFFF',
    borderRadius: 16,
    marginBottom: 20,
  },
  emptyText: {
    color: muted,
    textAlign: 'center',
  },
  insightCard: {
    flexDirection: 'row',
    backgroundColor: '#E6F3EB',
    padding: 17,
    borderRadius: 19,
    marginTop: 16,
    marginBottom: 22,
  },
  insightIcon: {
    width: 39,
    height: 39,
    borderRadius: 14,
    backgroundColor: '#CFE9D9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  insightEmoji: {
    color: green,
    fontSize: 23,
    fontWeight: '800',
  },
  insightContent: {
    flex: 1,
    marginLeft: 12,
  },
  insightTitle: {
    color: green,
    fontSize: 15,
    fontWeight: '800',
  },
  insightText: {
    color: '#57766A',
    fontSize: 12,
    lineHeight: 19,
    marginTop: 6,
  },
  insightLink: {
    color: green,
    fontSize: 12,
    fontWeight: '800',
    marginTop: 10,
  },
  forecastCard: {
    backgroundColor: '#FFFFFF',
    borderRadius: 20,
    padding: 18,
    borderWidth: 1,
    borderColor: '#E8EFE9',
  },
  forecastTop: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  forecastEyebrow: {
    color: green,
    fontSize: 10,
    fontWeight: '800',
    letterSpacing: 1,
  },
  forecastTitle: {
    color: dark,
    fontSize: 17,
    fontWeight: '800',
    marginTop: 7,
  },
  forecastEmoji: {
    fontSize: 29,
  },
  forecastDescription: {
    color: muted,
    fontSize: 12,
    lineHeight: 19,
    marginTop: 12,
  },
  forecastButton: {
    alignSelf: 'flex-start',
    backgroundColor: '#E2F1E6',
    borderRadius: 11,
    paddingHorizontal: 14,
    paddingVertical: 11,
    marginTop: 15,
  },
  forecastButtonText: {
    color: green,
    fontSize: 12,
    fontWeight: '800',
  },
  disclaimer: {
    color: muted,
    fontSize: 10,
    lineHeight: 16,
    textAlign: 'center',
    marginTop: 20,
    marginBottom: 10,
  },
  bottomNav: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#FFFFFF',
    borderTopWidth: 1,
    borderTopColor: '#E8EFE9',
    paddingTop: 10,
    paddingBottom: 8,
  },
  navItem: {
    flex: 1,
    alignItems: 'center',
    gap: 4,
  },
  navIcon: {
    color: '#94A59D',
    fontSize: 22,
    fontWeight: '700',
  },
  navLabel: {
    color: '#94A59D',
    fontSize: 10,
  },
  navActive: {
    color: green,
    fontWeight: '800',
  },
});
