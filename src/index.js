import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import App from "./App";
//import * as serviceWorker from './serviceWorker';
import { ChakraProvider, CSSReset } from '@chakra-ui/react';
import theme from './theme';
import PWAPrompt from 'react-ios-pwa-prompt';
import * as serviceWorkerRegistration from './serviceWorkerRegistration';
import reportWebVitals from "./reportWebVitals";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <ChakraProvider theme={theme}>
      <CSSReset />
      <App />
        <PWAPrompt
          promptOnVisit={1}
          timesToShow={3}
          copyClosePrompt="Close"
          permanentlyHideOnDismiss={false}
        />
    </ChakraProvider>
  </React.StrictMode>
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
// serviceWorker.register();
serviceWorkerRegistration.register();

reportWebVitals();
