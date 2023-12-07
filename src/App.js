import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/HomePage';
import Page2 from './Pages/Page2';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/page2" element={<Page2 />} />
        <Route path="/" element={<HomePage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
