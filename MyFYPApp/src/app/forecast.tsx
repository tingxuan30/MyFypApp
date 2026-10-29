import React, { useState } from 'react';
import { Alert, ScrollView, StatusBar, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

const green = '#087653';
const dark = '#173C32';
const muted = '#7B8D86';
const bg = '#F5F8F5';

const forecastData: Record<string, { price: string; change: string; direction: string; points: string[] }> = {
  Tomato: { price: 'RM 4.80', change: '−3.0%', direction: 'Potential decrease', points: ['4.95', '4.90', '4.86', '4.82', '4.80'] },
  Carrot: { price: 'RM 3.80', change: '+2.5%', direction: 'Potential increase', points: ['3.65', '3.68', '3.72', '3.76', '3.80'] },
  Cabbage: { price: 'RM 2.50', change: '−1.5%', direction: 'Potential decrease', points: ['2.58', '2.56', '2.54', '2.52', '2.50'] },
};

export default function ForecastScreen() {
  const [selected, setSelected] = useState('Tomato');
  const item = forecastData[selected];

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={bg} />
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View style={styles.brandIcon}><Text style={styles.brandEmoji}>📈</Text></View>
          <View style={styles.brandText}>
            <Text style={styles.brandName}>Price Forecast</Text>
            <Text style={styles.brandSubtitle}>Understand possible future price changes</Text>
          </View>
        </View>

        <View style={styles.hero}>
          <Text style={styles.eyebrow}>SMART PRICE PLANNING</Text>
          <Text style={styles.heroTitle}>When should you buy?</Text>
          <Text style={styles.heroDescription}>Explore an example forecast to see how historical price data could help you plan your next purchase.</Text>
        </View>

        <Text style={styles.sectionTitle}>Choose a vegetable</Text>
        <View style={styles.vegetableChoices}>
          {Object.keys(forecastData).map((name) => (
            <TouchableOpacity key={name} onPress={() => setSelected(name)} style={[styles.vegetableChoice, selected === name && styles.vegetableChoiceActive]}>
              <Text style={[styles.vegetableChoiceText, selected === name && styles.vegetableChoiceTextActive]}>{name}</Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.priceCard}>
          <View style={styles.cardTop}>
            <View>
              <Text style={styles.cardEyebrow}>ESTIMATED PRICE · DEMO</Text>
              <Text style={styles.price}>{item.price}<Text style={styles.perKg}> / kg</Text></Text>
            </View>
            <View style={styles.trendBadge}><Text style={styles.trendBadgeText}>{item.change}</Text></View>
          </View>
          <Text style={styles.direction}>{item.direction}</Text>
          <Text style={styles.mutedText}>Illustrative estimate only — not a real prediction.</Text>
        </View>

        <View style={styles.chartCard}>
          <Text style={styles.sectionTitle}>Possible price trend</Text>
          <Text style={styles.sectionSubtitle}>Example values · RM per kg</Text>
          <View style={styles.chart}>
            {item.points.map((value, index) => (
              <View key={`${selected}-${index}`} style={styles.chartColumn}>
                <Text style={styles.chartValue}>{value}</Text>
                <View style={[styles.bar, { height: 42 + Number(value) * 13 }]} />
                <Text style={styles.chartLabel}>{['Now', '+1', '+2', '+3', '+4'][index]}</Text>
              </View>
            ))}
          </View>
          <View style={styles.chartLegend}><View style={styles.legendDot} /><Text style={styles.legendText}>Illustrative future price path</Text></View>
        </View>

        <View style={styles.insightCard}>
          <Text style={styles.insightIcon}>✦</Text>
          <View style={styles.insightContent}>
            <Text style={styles.insightTitle}>How to use this forecast</Text>
            <Text style={styles.insightText}>Compare the estimate with recent prices and your shopping needs. The final system can generate forecasts after your historical dataset and prediction model are connected.</Text>
          </View>
        </View>

        <TouchableOpacity style={styles.primaryButton} onPress={() => Alert.alert('Forecast model', 'The prediction model is not connected yet. This page currently uses illustrative demo values.')}>
          <Text style={styles.primaryButtonText}>View Forecast Details  →</Text>
        </TouchableOpacity>
        <Text style={styles.disclaimer}>FYP prototype · Sample values only. Do not use these figures as actual market prices.</Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: bg },
  content: { paddingHorizontal: 20, paddingTop: 12, paddingBottom: 32 },
  header: { flexDirection: 'row', alignItems: 'center', marginBottom: 22 },
  brandIcon: { width: 46, height: 46, borderRadius: 15, backgroundColor: '#E0F1E6', alignItems: 'center', justifyContent: 'center' },
  brandEmoji: { fontSize: 25 },
  brandText: { flex: 1, marginLeft: 11 },
  brandName: { fontSize: 22, fontWeight: '800', color: dark },
  brandSubtitle: { fontSize: 11, color: muted, marginTop: 3 },
  hero: { backgroundColor: '#E1F2E8', borderRadius: 24, padding: 20, marginBottom: 24 },
  eyebrow: { color: green, fontSize: 10, fontWeight: '800', letterSpacing: 1.2, marginBottom: 12 },
  heroTitle: { color: dark, fontSize: 25, fontWeight: '800' },
  heroDescription: { color: '#57766A', fontSize: 13, lineHeight: 20, marginTop: 9 },
  sectionTitle: { color: dark, fontSize: 18, fontWeight: '800' },
  vegetableChoices: { flexDirection: 'row', gap: 8, marginTop: 12, marginBottom: 16 },
  vegetableChoice: { flex: 1, borderWidth: 1, borderColor: '#DCE8DF', backgroundColor: '#FFFFFF', paddingVertical: 12, borderRadius: 12, alignItems: 'center' },
  vegetableChoiceActive: { backgroundColor: green, borderColor: green },
  vegetableChoiceText: { color: muted, fontSize: 11, fontWeight: '700' },
  vegetableChoiceTextActive: { color: '#FFFFFF' },
  priceCard: { backgroundColor: '#FFFFFF', borderRadius: 19, borderWidth: 1, borderColor: '#E8EFE9', padding: 18, marginBottom: 16 },
  cardTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  cardEyebrow: { color: green, fontSize: 9, fontWeight: '800', letterSpacing: 0.8 },
  price: { color: dark, fontSize: 27, fontWeight: '800', marginTop: 8 },
  perKg: { color: muted, fontSize: 12, fontWeight: '400' },
  trendBadge: { backgroundColor: '#E2F1E6', borderRadius: 10, paddingHorizontal: 11, paddingVertical: 8 },
  trendBadgeText: { color: green, fontSize: 12, fontWeight: '800' },
  direction: { color: dark, fontSize: 13, fontWeight: '700', marginTop: 12 },
  mutedText: { color: muted, fontSize: 10, marginTop: 5 },
  chartCard: { backgroundColor: '#FFFFFF', borderRadius: 19, borderWidth: 1, borderColor: '#E8EFE9', padding: 17, marginBottom: 16 },
  sectionSubtitle: { color: muted, fontSize: 12, marginTop: 5 },
  chart: { flexDirection: 'row', alignItems: 'flex-end', justifyContent: 'space-around', height: 175, marginTop: 14 },
  chartColumn: { alignItems: 'center', justifyContent: 'flex-end', flex: 1, height: '100%' },
  chartValue: { color: muted, fontSize: 9, marginBottom: 5 },
  bar: { width: 24, maxHeight: 115, backgroundColor: '#8BC8A7', borderRadius: 7 },
  chartLabel: { color: muted, fontSize: 10, marginTop: 7 },
  chartLegend: { flexDirection: 'row', alignItems: 'center', marginTop: 12, gap: 7 },
  legendDot: { width: 8, height: 8, borderRadius: 4, backgroundColor: '#8BC8A7' },
  legendText: { color: muted, fontSize: 10 },
  insightCard: { flexDirection: 'row', backgroundColor: '#E6F3EB', padding: 16, borderRadius: 17, marginBottom: 16 },
  insightIcon: { color: green, fontSize: 23, fontWeight: '800', marginRight: 12 },
  insightContent: { flex: 1 },
  insightTitle: { color: green, fontSize: 14, fontWeight: '800' },
  insightText: { color: '#57766A', fontSize: 12, lineHeight: 19, marginTop: 6 },
  primaryButton: { backgroundColor: green, borderRadius: 13, paddingVertical: 14, alignItems: 'center' },
  primaryButtonText: { color: '#FFFFFF', fontSize: 13, fontWeight: '800' },
  disclaimer: { color: muted, fontSize: 10, lineHeight: 16, textAlign: 'center', marginTop: 18 },
});
