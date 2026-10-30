import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { PanResponder, Pressable, ScrollView, StyleSheet, Text, View, useWindowDimensions } from "react-native";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { useFocusEffect, useRouter } from "expo-router";
import { newGame, playMove } from "../src/game";

const DEFAULT_SETTINGS = { gridSize: 4, spawnValues: [2, 4] };
const TILE_COLORS = {
  0: "#101827",
  2: "#102A40",
  4: "#123B55",
  8: "#075B75",
  16: "#006F91",
  32: "#007FA8",
  64: "#008FC2",
  128: "#2448A8",
  256: "#4935A8",
  512: "#702B9C",
  1024: "#A52691",
  2048: "#E026A8",
};

export default function GameScreen() {
  const router = useRouter();
  const { width } = useWindowDimensions();
  const [settings, setSettings] = useState(DEFAULT_SETTINGS);
  const [game, setGame] = useState(() => newGame(4, [2, 4]));
  const [bestScore, setBestScore] = useState(0);
  const [loaded, setLoaded] = useState(false);
  const gameRef = useRef(game);

  useEffect(() => { gameRef.current = game; }, [game]);

  // Load saved settings each time the game screen becomes active.
  // Returning from Settings therefore applies the latest choices automatically.
  useFocusEffect(useCallback(() => {
    let active = true;
    async function loadSavedData() {
      try {
        const savedSettings = await AsyncStorage.getItem("gameSettings");
        const savedBest = await AsyncStorage.getItem("bestScore");
        const parsed = savedSettings ? JSON.parse(savedSettings) : DEFAULT_SETTINGS;
        const gridSize = [3, 4, 5, 6].includes(parsed.gridSize) ? parsed.gridSize : 4;
        const values = Array.isArray(parsed.spawnValues)
          ? parsed.spawnValues.filter((n) => [2, 4, 8, 16].includes(n)) : [2, 4];
        const safeSettings = { gridSize, spawnValues: values.length ? values : [2, 4] };
        if (active) {
          setSettings(safeSettings);
          setBestScore(savedBest ? Number(savedBest) || 0 : 0);
          // Start a fresh round so the saved settings apply to the new board.
          setGame(newGame(gridSize, safeSettings.spawnValues));
          setLoaded(true);
        }
      } catch {
        if (active) setLoaded(true);
      }
    }
    loadSavedData();
    return () => { active = false; };
  }, []));

  // Save the best score locally whenever the current score beats it.
  useEffect(() => {
    if (game.score > bestScore) {
      setBestScore(game.score);
      AsyncStorage.setItem("bestScore", String(game.score)).catch(() => {});
    }
  }, [game.score, bestScore]);

  function restartGame() {
    setGame(newGame(settings.gridSize, settings.spawnValues));
  }

  // Move the tiles in the requested direction.
  function handleMove(direction) {
    if (gameRef.current.over) return;
    setGame((current) => playMove(current, direction, settings.spawnValues));
  }

  // Detects a finger swipe and turns it into a direction.
  const panResponder = useMemo(() => PanResponder.create({
    onMoveShouldSetPanResponder: (_, gesture) => Math.abs(gesture.dx) > 12 || Math.abs(gesture.dy) > 12,
    onPanResponderRelease: (_, gesture) => {
      if (Math.max(Math.abs(gesture.dx), Math.abs(gesture.dy)) < 25) return;
      if (Math.abs(gesture.dx) > Math.abs(gesture.dy)) handleMove(gesture.dx > 0 ? "right" : "left");
      else handleMove(gesture.dy > 0 ? "down" : "up");
    },
  }), [settings.spawnValues]);

  const gap = 6;
  const boardWidth = Math.min(width - 36, 440);
  const cellSize = (boardWidth - gap * (settings.gridSize + 1)) / settings.gridSize;

  if (!loaded) return <View style={styles.center}><Text>Loading game...</Text></View>;

  return (
    <ScrollView contentContainerStyle={styles.page}>
      <View style={styles.header}>
        <Text style={styles.title}>2048</Text>
        <Pressable style={styles.settingsButton} onPress={() => router.push("/settings")}>
          <Text style={styles.settingsButtonText}>Settings</Text>
        </Pressable>
      </View>
      <Text style={styles.subtitle}>Join matching tiles to reach 2048.</Text>

      <View style={styles.scoreRow}>
        <View style={styles.scoreBox}><Text style={styles.scoreLabel}>SCORE</Text><Text style={styles.scoreValue}>{game.score}</Text></View>
        <View style={styles.scoreBox}><Text style={styles.scoreLabel}>BEST</Text><Text style={styles.scoreValue}>{bestScore}</Text></View>
        <Pressable style={styles.restartButton} onPress={restartGame}><Text style={styles.restartText}>New game</Text></Pressable>
      </View>

      <View style={[styles.board, { width: boardWidth, padding: gap, gap }]} {...panResponder.panHandlers}>
        {game.board.map((row, r) => (
          <View key={`row-${r}`} style={{ flexDirection: "row", gap }}>
            {row.map((value, c) => (
              <View key={`${r}-${c}`} style={[styles.tile, { width: cellSize, height: cellSize, backgroundColor: TILE_COLORS[value] || "#3c3a32" }]}>
                <Text adjustsFontSizeToFit numberOfLines={1} style={[styles.tileText, { fontSize: Math.max(12, cellSize * (value >= 1024 ? 0.25 : 0.32)), color: "#FFFFFF" }]}>{value || ""}</Text>
              </View>
            ))}
          </View>
        ))}
        {(game.over || game.won) && (
          <View style={styles.overlay}>
            <Text style={styles.overlayTitle}>{game.over ? "No more moves" : "You reached 2048!"}</Text>
            <Pressable style={styles.restartButton} onPress={restartGame}><Text style={styles.restartText}>Play again</Text></Pressable>
          </View>
        )}
      </View>

      <Text style={styles.instructions}>Swipe on the board or use the buttons below to move the tiles.</Text>
      <View style={styles.controls}>
        <View style={styles.controlSpacer} /><DirectionButton label="Up" onPress={() => handleMove("up")} /><View style={styles.controlSpacer} />
        <DirectionButton label="Left" onPress={() => handleMove("left")} />
        <DirectionButton label="Down" onPress={() => handleMove("down")} />
        <DirectionButton label="Right" onPress={() => handleMove("right")} />
      </View>
      <Text style={styles.footer}>Grid: {settings.gridSize} × {settings.gridSize} · New tiles: {settings.spawnValues.join(", ")}</Text>
    </ScrollView>
  );
}

// Button for moving tiles in one direction.
function DirectionButton({ label, onPress }) {
  return <Pressable style={styles.directionButton} onPress={onPress}><Text style={styles.directionText}>{label}</Text></Pressable>;
}


//CSS wannabe section 
//       VVV
const styles = StyleSheet.create({
  page: {
    flexGrow: 1,
    alignItems: "center",
    padding: 18,
    paddingBottom: 32,
    backgroundColor: "#080B16",
  },

  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#080B16",
  },

  header: {
    width: "100%",
    maxWidth: 440,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-between",
  },

  title: {
    fontSize: 52,
    fontWeight: "800",
    color: "#00E5FF",
    textShadowColor: "#00E5FF",
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 12,
  },

  settingsButton: {
    paddingVertical: 10,
    paddingHorizontal: 14,
    backgroundColor: "#101A2B",
    borderRadius: 7,
    borderWidth: 1.5,
    borderColor: "#00E5FF",
    elevation: 4,
  },

  settingsButtonText: {
    color: "#00E5FF",
    fontWeight: "700",
  },

  subtitle: {
    width: "100%",
    maxWidth: 440,
    color: "#A9B8D0",
    fontSize: 15,
    marginBottom: 18,
  },

  scoreRow: {
    width: "100%",
    maxWidth: 440,
    flexDirection: "row",
    alignItems: "stretch",
    gap: 8,
    marginBottom: 14,
  },

  scoreBox: {
    minWidth: 76,
    padding: 8,
    borderRadius: 6,
    backgroundColor: "#101A2B",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1,
    borderColor: "#244D70",
  },

  scoreLabel: {
    color: "#00E5FF",
    fontSize: 11,
    fontWeight: "700",
  },

  scoreValue: {
    color: "#FFFFFF",
    fontSize: 20,
    fontWeight: "800",
  },

  restartButton: {
    backgroundColor: "#241432",
    borderRadius: 6,
    paddingHorizontal: 13,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1.5,
    borderColor: "#FF35B8",
    elevation: 4,
  },

  restartText: {
    color: "#FF8BDC",
    fontWeight: "700",
  },

  board: {
    backgroundColor: "#0D1424",
    borderRadius: 10,
    position: "relative",
    borderWidth: 2,
    borderColor: "#00BFEF",
    elevation: 6,
  },

  tile: {
    borderRadius: 5,
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 1.5,
    borderColor: "#00DFFF",
    shadowColor: "#00E5FF",
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.7,
    shadowRadius: 5,
    elevation: 3,
  },

  tileText: {
    fontWeight: "800",
    textAlign: "center",
    width: "94%",
    color: "#FFFFFF",
    textShadowColor: "#00E5FF",
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 4,
  },

  instructions: {
    maxWidth: 360,
    textAlign: "center",
    marginTop: 18,
    marginBottom: 12,
    color: "#A9B8D0",
    lineHeight: 21,
  },

  controls: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    gap: 8,
    maxWidth: 320,
  },

  controlSpacer: {
    width: 84,
    height: 42,
  },

  directionButton: {
    width: 84,
    paddingVertical: 12,
    borderRadius: 6,
    backgroundColor: "#101A2B",
    alignItems: "center",
    borderWidth: 1.5,
    borderColor: "#00BFEF",
    elevation: 3,
  },

  directionText: {
    color: "#00E5FF",
    fontWeight: "700",
  },

  footer: {
    marginTop: 18,
    color: "#7F91AE",
    textAlign: "center",
  },

  overlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: "rgba(8,11,22,0.92)",
    alignItems: "center",
    justifyContent: "center",
    gap: 14,
    borderRadius: 8,
  },

  overlayTitle: {
    fontSize: 22,
    fontWeight: "800",
    color: "#00E5FF",
    textAlign: "center",
    textShadowColor: "#00E5FF",
    textShadowOffset: { width: 0, height: 0 },
    textShadowRadius: 8,
  },
});