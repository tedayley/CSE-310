import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

// The stack lets the game and settings live on separate screens.
export default function RootLayout() {
  return (
    <>
      <StatusBar style="dark" />
      <Stack screenOptions={{ headerShown: false }} />
    </>
  );
}
