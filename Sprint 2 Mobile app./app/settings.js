import React, { useEffect, useState } from "react";
import { Alert, Pressable, ScrollView, StyleSheet, Text, View } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useRouter } from "expo-router";

const AVAILABLE_VALUES = [2, 4, 8, 16];

export default function SettingsScreen() {
  const router = useRouter();
  const [gridSize, setGridSize] = useState(4);
  const [spawnValues, setSpawnValues] = useState([2, 4]);
  const [loaded, setLoaded] = useState(false);

  // Load the saved choices when the settings screen opens.
  useEffect(() => {
    async function loadSettings() {
      try {
        const saved = await AsyncStorage.getItem("gameSettings");
        if (saved) {
          const parsed = JSON.parse(saved);
          if ([3, 4, 5, 6].includes(parsed.gridSize)) setGridSize(parsed.gridSize);
          if (Array.isArray(parsed.spawnValues)) {
            const valid = parsed.spawnValues.filter((n) => AVAILABLE_VALUES.includes(n));
            if (valid.length) setSpawnValues(valid);
          }
        }
      } catch {
        // Use the defaults if saved settings cannot be read.
      } finally {
        setLoaded(true);
      }
    }
    loadSettings();
  }, []);

  // Select or deselect a number that can appear as a new tile.
  function toggleSpawnValue(value) {
    setSpawnValues((current) => {
      if (current.includes(value)) {
        // Keep at least one possible value selected.
        if (current.length === 1) return current;
        return current.filter((item) => item !== value);
      }
      return [...current, value].sort((a, b) => a - b);
    });
  }

  // Save the choices on the phone and return to the game.
  async function saveSettings() {
    try {
      await AsyncStorage.setItem("gameSettings", JSON.stringify({ gridSize, spawnValues }));
      router.back();
    } catch {
      Alert.alert("Could not save", "Your settings could not be saved on this device.");
    }
  }

  if (!loaded) return <View style={styles.center}><Text>Loading settings...</Text></View>;

  return (
    <ScrollView contentContainerStyle={styles.page}>
      <View style={styles.header}>
        <Pressable onPress={() => router.back()} style={styles.backButton}><Text style={styles.backText}>Back</Text></Pressable>
        <Text style={styles.title}>Settings</Text>
      </View>

      <Text style={styles.sectionTitle}>Grid size</Text>
      <Text style={styles.description}>Choose the number of rows and columns.</Text>
      <View style={styles.optionsRow}>
        {[3, 4, 5, 6].map((size) => <OptionButton key={size} label={`${size} × ${size}`} selected={gridSize === size} onPress={() => setGridSize(size)} />)}
      </View>

      <Text style={styles.sectionTitle}>New tile values</Text>
      <Text style={styles.description}>Choose which numbers may appear in empty squares after a move. At least one value must remain selected.</Text>
      <View style={styles.optionsRow}>
        {AVAILABLE_VALUES.map((value) => <OptionButton key={value} label={String(value)} selected={spawnValues.includes(value)} onPress={() => toggleSpawnValue(value)} />)}
      </View>

      <View style={styles.note}><Text style={styles.noteText}>Saving settings starts a new round using your selected grid size and tile values.</Text></View>
      <Pressable style={styles.saveButton} onPress={saveSettings}><Text style={styles.saveText}>Save settings</Text></Pressable>
    </ScrollView>
  );
}

// Reusable option button with a different style when selected.
function OptionButton({ label, selected, onPress }) {
  return (
    <Pressable accessibilityRole="button" accessibilityState={{ selected }} onPress={onPress} style={[styles.option, selected && styles.optionSelected]}>
      <Text style={[styles.optionText, selected && styles.optionTextSelected]}>{label}</Text>
    </Pressable>
  );
}


//CSS wannabe VVV
const styles = StyleSheet.create({
  page: { flexGrow: 1, backgroundColor: "#faf8ef", padding: 22, paddingTop: 36 },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  header: { flexDirection: "row", alignItems: "center", gap: 18, marginBottom: 30 },
  backButton: { paddingVertical: 9, paddingHorizontal: 13, borderRadius: 6, backgroundColor: "#8f7a66" },
  backText: { color: "#ffffff", fontWeight: "700" },
  title: { fontSize: 32, fontWeight: "800", color: "#776e65" },
  sectionTitle: { marginTop: 12, fontSize: 21, fontWeight: "800", color: "#776e65" },
  description: { marginTop: 7, marginBottom: 14, color: "#776e65", lineHeight: 21 },
  optionsRow: { flexDirection: "row", flexWrap: "wrap", gap: 10, marginBottom: 20 },
  option: { minWidth: 66, paddingVertical: 13, paddingHorizontal: 14, borderWidth: 2, borderColor: "#bbada0", borderRadius: 7, alignItems: "center", backgroundColor: "#ffffff" },
  optionSelected: { backgroundColor: "#8f7a66", borderColor: "#8f7a66" },
  optionText: { color: "#776e65", fontWeight: "700", fontSize: 16 },
  optionTextSelected: { color: "#ffffff" },
  note: { padding: 14, backgroundColor: "#eee4da", borderRadius: 7, marginTop: 4, marginBottom: 22 },
  noteText: { color: "#776e65", lineHeight: 21 },
  saveButton: { padding: 15, borderRadius: 7, backgroundColor: "#8f7a66", alignItems: "center" },
  saveText: { color: "#ffffff", fontSize: 16, fontWeight: "800" },
});
