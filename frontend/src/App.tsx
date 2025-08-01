import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { ChordAnalyzerPage } from './pages/ChordAnalyzerPage';
import { ScaleAnalyzerPage } from './pages/ScaleAnalyzerPage';
import { FamousProgressionsPage } from './pages/FamousProgressionsPage';
import { Navigation } from './components/Navigation';
import './App.css';

function App() {
  return (
    // BrowserRouterでアプリ全体を囲むことで、ルーティング機能を有効化
    <BrowserRouter>
      {/* 全ページ共通のタイトル */}
      <h1>My Music App</h1>
      
      {/* 全ページ共通のナビゲーションタブ */}
      <Navigation />

      {/* URLに応じて表示するページを切り替える設定 */}
      <Routes>
        {/* ルートURL ("/") にはコード分析ページを表示 */}
        <Route path="/cord-analyzer" element={<ChordAnalyzerPage />} />
        
        {/* "/scale-analyzer" というURLにはスケール分析ページを表示 */}
        <Route path="/scale-analyzer" element={<ScaleAnalyzerPage />} />

        <Route path="/progressions" element={<FamousProgressionsPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;