import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomePage } from './pages/HomePage'; // <-- HomePageをインポート
import { ChordAnalyzerPage } from './pages/ChordAnalyzerPage';
import { ScaleAnalyzerPage } from './pages/ScaleAnalyzerPage';
import { FamousProgressionsPage } from './pages/FamousProgressionsPage';
import { Navigation } from './components/Navigation';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <h1>My Music App</h1>
      
      <Navigation />

      {/* ↓↓↓ URLとページの対応を、新しい構成に更新 ↓↓↓ */}
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chord-analyzer" element={<ChordAnalyzerPage />} />
        <Route path="/scale-analyzer" element={<ScaleAnalyzerPage />} />
        <Route path="/progressions" element={<FamousProgressionsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;