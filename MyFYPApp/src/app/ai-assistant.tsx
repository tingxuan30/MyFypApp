import React, { useState } from 'react';
import { Alert, KeyboardAvoidingView, Platform, ScrollView, StatusBar, StyleSheet, Text, TextInput, TouchableOpacity, View } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

type Message = { id: number; text: string; from: 'assistant' | 'user' };

const green = '#087653';
const dark = '#173C32';
const muted = '#7B8D86';
const bg = '#F5F8F5';

const suggestions = [
  'Which vegetables are cheaper?',
  'Explain price trends',
  'When should I buy tomatoes?',
];

export default function AIAssistantScreen() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, from: 'assistant', text: 'Hi! I’m your VegPrice MY assistant. You can ask me about vegetable prices, market trends and possible price changes.' },
  ]);

  const sendMessage = (question = input) => {
    const trimmed = question.trim();
    if (!trimmed) return;
    const reply = 'Thanks for your question! In the completed app, I will use the prepared vegetable price dataset to answer this. AI responses and real price data have not been connected yet.';
    setMessages((current) => [
      ...current,
      { id: Date.now(), from: 'user', text: trimmed },
      { id: Date.now() + 1, from: 'assistant', text: reply },
    ]);
    setInput('');
  };

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor={bg} />
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined} keyboardVerticalOffset={90}>
        <View style={styles.content}>
          <View style={styles.header}>
            <View style={styles.brandIcon}><Text style={styles.brandEmoji}>✦</Text></View>
            <View style={styles.brandText}>
              <Text style={styles.brandName}>AI Assistant</Text>
              <Text style={styles.brandSubtitle}>Your smart vegetable market guide</Text>
            </View>
            <View style={styles.statusPill}><View style={styles.statusDot} /><Text style={styles.statusText}>DEMO</Text></View>
          </View>

          <View style={styles.hero}>
            <Text style={styles.eyebrow}>ASK VEGPRICE MY</Text>
            <Text style={styles.heroTitle}>Let’s make sense of prices.</Text>
            <Text style={styles.heroDescription}>Ask questions about recent prices, trends or possible times to buy.</Text>
          </View>

          <Text style={styles.sectionTitle}>Suggested questions</Text>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.suggestionRow}>
            {suggestions.map((suggestion) => (
              <TouchableOpacity key={suggestion} style={styles.suggestionChip} onPress={() => sendMessage(suggestion)}>
                <Text style={styles.suggestionText}>{suggestion}</Text>
              </TouchableOpacity>
            ))}
          </ScrollView>

          <View style={styles.chatHeader}>
            <Text style={styles.sectionTitle}>Conversation</Text>
            <TouchableOpacity onPress={() => setMessages([{ id: Date.now(), from: 'assistant', text: 'Hello! What would you like to know about Malaysian vegetable prices?' }])}>
              <Text style={styles.clearChat}>Clear chat</Text>
            </TouchableOpacity>
          </View>

          <ScrollView style={styles.messageList} contentContainerStyle={styles.messageContent} showsVerticalScrollIndicator={false}>
            {messages.map((message) => (
              <View key={message.id} style={[styles.messageRow, message.from === 'user' && styles.userMessageRow]}>
                {message.from === 'assistant' && <View style={styles.avatar}><Text style={styles.avatarText}>✦</Text></View>}
                <View style={[styles.messageBubble, message.from === 'user' ? styles.userBubble : styles.assistantBubble]}>
                  <Text style={[styles.messageText, message.from === 'user' && styles.userMessageText]}>{message.text}</Text>
                </View>
              </View>
            ))}
          </ScrollView>

          <View style={styles.inputRow}>
            <TextInput
              style={styles.chatInput}
              placeholder="Ask about vegetable prices..."
              placeholderTextColor="#91A19A"
              value={input}
              onChangeText={setInput}
              onSubmitEditing={() => sendMessage()}
              returnKeyType="send"
            />
            <TouchableOpacity style={styles.sendButton} onPress={() => sendMessage()}>
              <Text style={styles.sendButtonText}>↑</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.disclaimer}>Prototype only · AI is not connected to live data or a language model yet.</Text>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: bg },
  flex: { flex: 1 },
  content: { flex: 1, paddingHorizontal: 20, paddingTop: 12, paddingBottom: 8 },
  header: { flexDirection: 'row', alignItems: 'center', marginBottom: 18 },
  brandIcon: { width: 46, height: 46, borderRadius: 15, backgroundColor: '#E0F1E6', alignItems: 'center', justifyContent: 'center' },
  brandEmoji: { color: green, fontSize: 26, fontWeight: '800' },
  brandText: { flex: 1, marginLeft: 11 },
  brandName: { fontSize: 22, fontWeight: '800', color: dark },
  brandSubtitle: { fontSize: 11, color: muted, marginTop: 3 },
  statusPill: { flexDirection: 'row', alignItems: 'center', gap: 5, backgroundColor: '#E2F1E6', borderRadius: 8, paddingHorizontal: 8, paddingVertical: 6 },
  statusDot: { width: 6, height: 6, borderRadius: 3, backgroundColor: green },
  statusText: { color: green, fontSize: 9, fontWeight: '800' },
  hero: { backgroundColor: '#E1F2E8', borderRadius: 22, padding: 18, marginBottom: 18 },
  eyebrow: { color: green, fontSize: 10, fontWeight: '800', letterSpacing: 1.2, marginBottom: 10 },
  heroTitle: { color: dark, fontSize: 23, fontWeight: '800' },
  heroDescription: { color: '#57766A', fontSize: 12, lineHeight: 18, marginTop: 7 },
  sectionTitle: { color: dark, fontSize: 16, fontWeight: '800' },
  suggestionRow: { gap: 8, paddingVertical: 11, paddingRight: 4 },
  suggestionChip: { backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#DCE8DF', borderRadius: 15, paddingHorizontal: 12, paddingVertical: 10 },
  suggestionText: { color: green, fontSize: 11, fontWeight: '700' },
  chatHeader: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginTop: 3, marginBottom: 10 },
  clearChat: { color: green, fontSize: 11, fontWeight: '700' },
  messageList: { flex: 1, backgroundColor: '#FFFFFF', borderRadius: 18, borderWidth: 1, borderColor: '#E8EFE9' },
  messageContent: { padding: 12, gap: 12 },
  messageRow: { flexDirection: 'row', alignItems: 'flex-end', gap: 7 },
  userMessageRow: { justifyContent: 'flex-end' },
  avatar: { width: 27, height: 27, borderRadius: 10, backgroundColor: '#E0F1E6', alignItems: 'center', justifyContent: 'center' },
  avatarText: { color: green, fontWeight: '800' },
  messageBubble: { maxWidth: '85%', paddingHorizontal: 12, paddingVertical: 10, borderRadius: 15 },
  assistantBubble: { backgroundColor: '#F0F6EF', borderBottomLeftRadius: 5 },
  userBubble: { backgroundColor: green, borderBottomRightRadius: 5 },
  messageText: { color: dark, fontSize: 12, lineHeight: 18 },
  userMessageText: { color: '#FFFFFF' },
  inputRow: { flexDirection: 'row', alignItems: 'center', gap: 8, marginTop: 10 },
  chatInput: { flex: 1, minHeight: 47, backgroundColor: '#FFFFFF', borderWidth: 1, borderColor: '#E8EFE9', borderRadius: 14, paddingHorizontal: 13, color: dark, fontSize: 12 },
  sendButton: { width: 47, height: 47, borderRadius: 14, backgroundColor: green, alignItems: 'center', justifyContent: 'center' },
  sendButtonText: { color: '#FFFFFF', fontSize: 25, fontWeight: '700', marginTop: -2 },
  disclaimer: { color: muted, fontSize: 9, textAlign: 'center', marginTop: 8, marginBottom: 2 },
});
