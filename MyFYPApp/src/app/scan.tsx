import React, { useState } from 'react';
import { Alert, ScrollView, StatusBar, StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

const green = '#087653';
const dark = '#173C32';
const muted = '#7B8D86';
const bg = '#F5F8F5';

export default function ScanScreen() {
  const [selected, setSelected] = useState('Tomato');

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={bg} />
      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View style={styles.brandIcon}><Text style={styles.brandEmoji}>📷</Text></View>
          <View style={styles.brandText}>
            <Text style={styles.brandName}>Scan Vegetable</Text>
            <Text style={styles.brandSubtitle}>Identify a vegetable and check its price</Text>
          </View>
        </View>

        <View style={styles.hero}>
          <Text style={styles.eyebrow}>SMART VEGETABLE SCANNER</Text>
          <Text style={styles.heroTitle}>Point. Scan. Discover.</Text>
          <Text style={styles.heroDescription}>Use the camera to identify a vegetable and view its price information.</Text>
        </View>

        <View style={styles.scanPanel}>
          <View style={styles.scanFrame}>
            <Text style={styles.scanEmoji}>🥦</Text>
            <View style={[styles.corner, styles.topLeft]} />
            <View style={[styles.corner, styles.topRight]} />
            <View style={[styles.corner, styles.bottomLeft]} />
            <View style={[styles.corner, styles.bottomRight]} />
          </View>
          <Text style={styles.panelTitle}>Camera scanner</Text>
          <Text style={styles.panelDescription}>Camera recognition will be connected in a later development phase.</Text>
          <TouchableOpacity
            style={styles.primaryButton}
            onPress={() => Alert.alert('Camera not connected yet', 'This is the Scan page prototype. Camera permission and image recognition can be added next.')}
          >
            <Text style={styles.primaryButtonText}>📷  Open Camera</Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={styles.secondaryButton}
            onPress={() => Alert.alert('Upload image', 'Image upload can be connected when the scanning feature is implemented.')}
          >
            <Text style={styles.secondaryButtonText}>Choose from Photos</Text>
          </TouchableOpacity>
        </View>

        <Text style={styles.sectionTitle}>Try a sample result</Text>
        <Text style={styles.sectionSubtitle}>Preview how a scan result could look.</Text>
        <View style={styles.sampleCard}>
          <View style={styles.sampleEmojiBox}><Text style={styles.sampleEmoji}>{selected === 'Tomato' ? '🍅' : selected === 'Carrot' ? '🥕' : '🥬'}</Text></View>
          <View style={styles.sampleInfo}>
            <Text style={styles.sampleName}>{selected}</Text>
            <Text style={styles.sampleCaption}>Example average price</Text>
            <Text style={styles.samplePrice}>{selected === 'Tomato' ? 'RM 4.80' : selected === 'Carrot' ? 'RM 3.80' : 'RM 3.20'} <Text style={styles.perKg}>/ kg</Text></Text>
          </View>
          <Text style={styles.demoLabel}>DEMO</Text>
        </View>
        <View style={styles.choiceRow}>
          {['Tomato', 'Carrot', 'Kangkung'].map((name) => (
            <TouchableOpacity key={name} style={[styles.choice, selected === name && styles.choiceActive]} onPress={() => setSelected(name)}>
              <Text style={[styles.choiceText, selected === name && styles.choiceTextActive]}>{name}</Text>
            </TouchableOpacity>
          ))}
        </View>
        <View style={styles.noteCard}>
          <Text style={styles.noteTitle}>How it will work</Text>
          <Text style={styles.noteText}>1. Take or upload a vegetable photo{"\n"}2. AI identifies the vegetable{"\n"}3. The app displays matching price trends from your dataset</Text>
        </View>
        <Text style={styles.disclaimer}>FYP prototype · Sample result only. No image recognition is active yet.</Text>
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
  hero: { backgroundColor: '#E1F2E8', borderRadius: 24, padding: 20, marginBottom: 20 },
  eyebrow: { color: green, fontSize: 10, fontWeight: '800', letterSpacing: 1.2, marginBottom: 12 },
  heroTitle: { color: dark, fontSize: 25, fontWeight: '800' },
  heroDescription: { color: '#57766A', fontSize: 13, lineHeight: 20, marginTop: 9 },
  scanPanel: { backgroundColor: '#FFFFFF', borderRadius: 22, borderWidth: 1, borderColor: '#E8EFE9', padding: 18, alignItems: 'center', marginBottom: 25 },
  scanFrame: { width: 190, height: 190, borderRadius: 25, backgroundColor: '#F0F6EF', alignItems: 'center', justifyContent: 'center', position: 'relative', marginBottom: 18 },
  scanEmoji: { fontSize: 75 },
  corner: { position: 'absolute', width: 30, height: 30, borderColor: green },
  topLeft: { top: 13, left: 13, borderTopWidth: 3, borderLeftWidth: 3, borderTopLeftRadius: 8 },
  topRight: { top: 13, right: 13, borderTopWidth: 3, borderRightWidth: 3, borderTopRightRadius: 8 },
  bottomLeft: { bottom: 13, left: 13, borderBottomWidth: 3, borderLeftWidth: 3, borderBottomLeftRadius: 8 },
  bottomRight: { bottom: 13, right: 13, borderBottomWidth: 3, borderRightWidth: 3, borderBottomRightRadius: 8 },
  panelTitle: { color: dark, fontSize: 17, fontWeight: '800' },
  panelDescription: { color: muted, fontSize: 12, textAlign: 'center', lineHeight: 18, marginTop: 7, marginBottom: 16 },
  primaryButton: { width: '100%', backgroundColor: green, paddingVertical: 14, borderRadius: 13, alignItems: 'center' },
  primaryButtonText: { color: '#FFFFFF', fontSize: 13, fontWeight: '800' },
  secondaryButton: { paddingVertical: 13, alignItems: 'center' },
  secondaryButtonText: { color: green, fontSize: 12, fontWeight: '700' },
  sectionTitle: { color: dark, fontSize: 19, fontWeight: '800' },
  sectionSubtitle: { color: muted, fontSize: 12, marginTop: 5, marginBottom: 13 },
  sampleCard: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#FFFFFF', borderRadius: 17, borderWidth: 1, borderColor: '#E8EFE9', padding: 12 },
  sampleEmojiBox: { width: 53, height: 53, borderRadius: 15, backgroundColor: '#F0F6EF', alignItems: 'center', justifyContent: 'center' },
  sampleEmoji: { fontSize: 28 },
  sampleInfo: { flex: 1, marginLeft: 12 },
  sampleName: { color: dark, fontSize: 14, fontWeight: '800' },
  sampleCaption: { color: muted, fontSize: 10, marginTop: 3 },
  samplePrice: { color: dark, fontSize: 16, fontWeight: '800', marginTop: 4 },
  perKg: { color: muted, fontSize: 11, fontWeight: '400' },
  demoLabel: { color: green, backgroundColor: '#E2F1E6', paddingHorizontal: 8, paddingVertical: 5, borderRadius: 7, fontSize: 9, fontWeight: '800' },
  choiceRow: { flexDirection: 'row', gap: 8, marginTop: 12, marginBottom: 18 },
  choice: { flex: 1, borderWidth: 1, borderColor: '#DCE8DF', backgroundColor: '#FFFFFF', paddingVertical: 10, borderRadius: 12, alignItems: 'center' },
  choiceActive: { backgroundColor: green, borderColor: green },
  choiceText: { color: muted, fontSize: 11, fontWeight: '700' },
  choiceTextActive: { color: '#FFFFFF' },
  noteCard: { backgroundColor: '#E6F3EB', padding: 16, borderRadius: 17 },
  noteTitle: { color: green, fontWeight: '800', fontSize: 13 },
  noteText: { color: '#57766A', fontSize: 12, lineHeight: 21, marginTop: 8 },
  disclaimer: { color: muted, fontSize: 10, lineHeight: 16, textAlign: 'center', marginTop: 18 },
});
