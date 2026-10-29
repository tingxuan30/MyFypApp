import React, { useMemo, useState } from 'react';
import {
  ScrollView,
  StatusBar,
  StyleSheet,
  Text,
  TextInput,
  TouchableOpacity,
  View,
  Alert,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

type Vegetable = {
  name: string;
  emoji: string;
  price: number;
  change: number;
  category: string;
};

const vegetables: Vegetable[] = [
  { name: 'Tomato', emoji: '🍅', price: 4.8, change: -6.3, category: 'Fruit vegetable' },
  { name: 'Kangkung', emoji: '🥬', price: 3.2, change: 4.1, category: 'Leafy vegetable' },
  { name: 'Cabbage', emoji: '🥬', price: 2.5, change: -2.8, category: 'Leafy vegetable' },
  { name: 'Carrot', emoji: '🥕', price: 3.8, change: 3.5, category: 'Root vegetable' },
  { name: 'Cucumber', emoji: '🥒', price: 3.1, change: -1.2, category: 'Fruit vegetable' },
  { name: 'Spinach', emoji: '🥬', price: 4.2, change: 2.0, category: 'Leafy vegetable' },
];

const green = '#087653';
const dark = '#173C32';
const muted = '#7B8D86';
const bg = '#F5F8F5';

export default function VegetablesScreen() {
  const [search, setSearch] = useState('');
  const [category, setCategory] = useState('All');

  const filtered = useMemo(() => vegetables.filter((item) => {
    const matchesSearch = item.name.toLowerCase().includes(search.toLowerCase());
    const matchesCategory = category === 'All' || item.category === category;
    return matchesSearch && matchesCategory;
  }), [search, category]);

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={bg} />
      <ScrollView showsVerticalScrollIndicator={false} contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View style={styles.brandIcon}><Text style={styles.brandEmoji}>🥬</Text></View>
          <View style={styles.brandText}>
            <Text style={styles.brandName}>Vegetables</Text>
            <Text style={styles.brandSubtitle}>Explore Malaysian vegetable prices</Text>
          </View>
        </View>

        <View style={styles.hero}>
          <Text style={styles.eyebrow}>VEGETABLE DIRECTORY</Text>
          <Text style={styles.heroTitle}>Find your vegetables.</Text>
          <Text style={styles.heroDescription}>
            Search the list to compare sample prices and recent price movements.
          </Text>
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

        <Text style={styles.sectionTitle}>Browse by category</Text>
        <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.chipRow}>
          {['All', 'Leafy vegetable', 'Root vegetable', 'Fruit vegetable'].map((item) => (
            <TouchableOpacity
              key={item}
              onPress={() => setCategory(item)}
              style={[styles.chip, category === item && styles.chipActive]}
            >
              <Text style={[styles.chipText, category === item && styles.chipTextActive]}>{item}</Text>
            </TouchableOpacity>
          ))}
        </ScrollView>

        <View style={styles.sectionHeader}>
          <View>
            <Text style={styles.sectionTitle}>Vegetable Prices</Text>
            <Text style={styles.sectionSubtitle}>{filtered.length} vegetables · Sample RM per kg</Text>
          </View>
          <Text style={styles.demoLabel}>DEMO DATA</Text>
        </View>

        {filtered.length === 0 ? (
          <View style={styles.emptyBox}><Text style={styles.emptyText}>No vegetables found. Try another search.</Text></View>
        ) : filtered.map((item) => (
          <TouchableOpacity
            key={item.name}
            style={styles.vegetableCard}
            onPress={() => Alert.alert(item.name, `Sample price: RM ${item.price.toFixed(2)}/kg\nWeekly change: ${item.change > 0 ? '+' : ''}${item.change}%`)}
          >
            <View style={styles.vegetableEmojiBox}><Text style={styles.vegetableEmoji}>{item.emoji}</Text></View>
            <View style={styles.vegetableInfo}>
              <Text style={styles.vegetableName}>{item.name}</Text>
              <Text style={styles.categoryText}>{item.category}</Text>
              <Text style={styles.vegetablePrice}>RM {item.price.toFixed(2)}<Text style={styles.perKg}> / kg</Text></Text>
            </View>
            <View style={styles.changeBox}>
              <Text style={[styles.changeValue, { color: item.change <= 0 ? green : '#D65A4A' }]}>
                {item.change <= 0 ? '↓ ' : '↑ '}{Math.abs(item.change).toFixed(1)}%
              </Text>
              <Text style={styles.changeCaption}>vs last week</Text>
            </View>
          </TouchableOpacity>
        ))}

        <View style={styles.noteCard}>
          <Text style={styles.noteTitle}>🌱 Price data note</Text>
          <Text style={styles.noteText}>These are demonstration values only. Connect your cleaned dataset later to show verified prices.</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: bg },
  content: { paddingHorizontal: 20, paddingTop: 12, paddingBottom: 32 },
  header: { flexDirection: 'row', alignItems: 'center', marginBottom: 22 },
  brandIcon: { width: 46, height: 46, borderRadius: 15, backgroundColor: '#E0F1E6', alignItems: 'center', justifyContent: 'center' },
  brandEmoji: { fontSize: 27 },
  brandText: { flex: 1, marginLeft: 11 },
  brandName: { fontSize: 23, fontWeight: '800', color: dark },
  brandSubtitle: { fontSize: 11, color: muted, marginTop: 3 },
  hero: { backgroundColor: '#E1F2E8', borderRadius: 24, padding: 20, marginBottom: 24 },
  eyebrow: { color: green, fontSize: 10, fontWeight: '800', letterSpacing: 1.2, marginBottom: 12 },
  heroTitle: { color: dark, fontSize: 25, fontWeight: '800' },
  heroDescription: { color: '#57766A', fontSize: 13, lineHeight: 20, marginTop: 8, marginBottom: 16 },
  searchBox: { minHeight: 48, flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFFFF', borderRadius: 13, paddingHorizontal: 13 },
  searchIcon: { color: muted, fontSize: 25, marginRight: 8 },
  searchInput: { flex: 1, color: dark, fontSize: 13, paddingVertical: 10 },
  clearText: { color: muted, padding: 5 },
  sectionTitle: { color: dark, fontSize: 18, fontWeight: '800' },
  chipRow: { gap: 8, paddingVertical: 13, paddingRight: 4 },
  chip: { borderWidth: 1, borderColor: '#DCE8DF', backgroundColor: '#FFFFFF', paddingHorizontal: 13, paddingVertical: 9, borderRadius: 20 },
  chipActive: { backgroundColor: green, borderColor: green },
  chipText: { color: muted, fontSize: 11, fontWeight: '600' },
  chipTextActive: { color: '#FFFFFF' },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 12, marginBottom: 14 },
  sectionSubtitle: { color: muted, fontSize: 12, marginTop: 5 },
  demoLabel: { color: green, backgroundColor: '#E2F1E6', paddingHorizontal: 9, paddingVertical: 6, borderRadius: 8, fontSize: 9, fontWeight: '800' },
  vegetableCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFFFF', borderRadius: 17, borderWidth: 1, borderColor: '#E8EFE9', padding: 12, marginBottom: 10 },
  vegetableEmojiBox: { width: 53, height: 53, borderRadius: 15, backgroundColor: '#F0F6EF', alignItems: 'center', justifyContent: 'center' },
  vegetableEmoji: { fontSize: 28 },
  vegetableInfo: { flex: 1, marginLeft: 12 },
  vegetableName: { color: dark, fontSize: 14, fontWeight: '700' },
  categoryText: { color: muted, fontSize: 10, marginTop: 3 },
  vegetablePrice: { color: dark, fontSize: 15, fontWeight: '800', marginTop: 4 },
  perKg: { color: muted, fontSize: 11, fontWeight: '400' },
  changeBox: { alignItems: 'flex-end', marginLeft: 5 },
  changeValue: { fontSize: 13, fontWeight: '800' },
  changeCaption: { color: muted, fontSize: 9, marginTop: 5 },
  emptyBox: { padding: 24, backgroundColor: '#FFFFFF', borderRadius: 16 },
  emptyText: { color: muted, textAlign: 'center' },
  noteCard: { backgroundColor: '#E6F3EB', padding: 16, borderRadius: 17, marginTop: 15 },
  noteTitle: { color: green, fontWeight: '800', fontSize: 13 },
  noteText: { color: '#57766A', fontSize: 12, lineHeight: 19, marginTop: 7 },
});
