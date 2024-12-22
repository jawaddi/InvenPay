import React from "react";
import ReactDOM from "react-dom/client"; // Use the new API
import "./index.css";
import App from "./App";
import reportWebVitals from "./reportWebVitals";

// Get the root DOM element
const rootElement = document.getElementById("root");

// Create a root and render the app
const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Optional: Measure app performance
reportWebVitals();
