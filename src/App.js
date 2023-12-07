import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import Page2 from './Pages/Page2';
import './App.css';

import { Amplify } from 'aws-amplify';

import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import config from './amplifyconfiguration.json';
Amplify.configure(config);

function App({ signOut, user }) {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/page2" element={<Page2 />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default withAuthenticator(App);
