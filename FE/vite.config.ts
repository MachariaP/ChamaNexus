import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  // Load env file based on `mode` in the current directory
  const env = loadEnv(mode, process.cwd(), '')
  
  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true,
      proxy: {
        // Proxy API requests to the backend in development
        '/api': {
          target: env.VITE_API_BASE_URL?.replace(/\/api\/v1$/, '') || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
          rewrite: (path) => path,
        },
        // Proxy direct requests (without /api prefix) for backward compatibility
        '/accounts': {
          target: env.VITE_API_BASE_URL?.replace(/\/api\/v1$/, '') || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
        '/csrf-token': {
          target: env.VITE_API_BASE_URL?.replace(/\/api\/v1$/, '') || 'http://localhost:8000',
          changeOrigin: true,
          secure: false,
        },
      },
    },
    build: {
      outDir: 'dist',
      sourcemap: false,
      minify: 'terser',
      terserOptions: {
        compress: {
          drop_console: mode === 'production',
          drop_debugger: true,
        },
      },
      rollupOptions: {
        output: {
          manualChunks: {
            'react-vendor': ['react', 'react-dom', 'react-router-dom'],
            'ui-vendor': ['@radix-ui/react-dialog', '@radix-ui/react-dropdown-menu'],
          },
        },
      },
    },
    base: '/',
  }
})
