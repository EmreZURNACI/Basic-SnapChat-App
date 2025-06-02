import React from "react";
import { Provider } from "react-redux";
import store from "./redux/store"; // store dosyan doğru yol ve isme sahip mi?
import { DripsyProvider, makeTheme } from "dripsy";
import HomeScreen from "./screens/HomeScreen";

const theme = makeTheme({
  colors: {
    background: "#ffffff",
    primary: "#2563eb", // mavi
    success: "#16a34a", // yeşil
    textGray: "#6b7280",
    white: "#ffffff",
  },
  radii: {
    xl: 16,
  },
  space: {
    4: 16,
    5: 20,
    6: 24,
  },
  text: {
    lg: {
      fontSize: 18,
    },
    semiboldWhite: {
      fontWeight: "600",
      color: "white",
    },
    gray500: {
      color: "textGray",
      fontSize: 18,
    },
  },
  sizes: {
    image: 256, // 64 * 4 (tailwind -> 16px * 64 = 1024px değil! Burada 256 olarak kullan)
  },
});

export default function App() {
  return (
    <Provider store={store}>
      <DripsyProvider theme={theme}>
        <HomeScreen />
      </DripsyProvider>
    </Provider>
  );
}
