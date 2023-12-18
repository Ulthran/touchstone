import './App.css';

import { Amplify } from 'aws-amplify';
import { withAuthenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import config from './amplifyconfiguration.json';
import HomePage from './Pages/HomePage';
Amplify.configure(config);

function App() {
  return (
    <div className='bg-gray-100 text-gray-800 font-sans min-h-screen flex flex-col'>
      <HomePage />
    </div>
  );
}

export default withAuthenticator(App);