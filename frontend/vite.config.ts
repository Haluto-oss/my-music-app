import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  // ↓↓↓ この一行が、今回の問題を解決する鍵です ↓↓↓
  appType: 'spa'
})