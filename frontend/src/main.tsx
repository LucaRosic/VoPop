import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import 'bootstrap/dist/css/bootstrap.css'; // Bootstrap
import { BrowserRouter } from 'react-router-dom';
import { StyledEngineProvider } from '@mui/material';

/*

  This is just the main file that starts up and renders our web application

*/

ReactDOM.createRoot(document.getElementById('root')!).render(
  
  <React.StrictMode>
    <BrowserRouter>
      <StyledEngineProvider injectFirst>
        <App />
      </StyledEngineProvider>
    </BrowserRouter>
  </React.StrictMode>,
)
