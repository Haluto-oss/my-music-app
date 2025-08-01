import { Link } from 'react-router-dom';

export function Navigation() {
  const navLinkStyle = { marginRight: '1rem', fontSize: '1.2em' };

  return (
    <nav style={{ marginBottom: '2rem', borderBottom: '1px solid #555', paddingBottom: '1rem' }}>
      {/* ↓↓↓ 「ホーム」へのリンクを追加し、「コード分析」のリンク先を変更 ↓↓↓ */}
      <Link to="/" style={navLinkStyle}>ホーム</Link>
      <Link to="/chord-analyzer" style={navLinkStyle}>コード分析</Link>
      <Link to="/scale-analyzer" style={navLinkStyle}>スケール分析</Link>
      <Link to="/progressions" style={navLinkStyle}>有名コード進行</Link>
    </nav>
  );
}