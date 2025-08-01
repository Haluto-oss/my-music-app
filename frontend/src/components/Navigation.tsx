// src/components/Navigation.tsx

import { Link } from 'react-router-dom';

export function Navigation() {
  return (
    <nav style={{ marginBottom: '2rem', borderBottom: '1px solid #555', paddingBottom: '1rem' }}>
      <Link to="/" style={{ marginRight: '1rem', fontSize: '1.2em' }}>コード分析</Link>
      <Link to="/scale-analyzer" style={{ fontSize: '1.2em' }}>スケール分析</Link>
      <Link to="/progressions" style={{ fontSize: '1.2em' }}>有名コード進行</Link>
    </nav>
  );
}