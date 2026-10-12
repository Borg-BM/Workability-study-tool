import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// Vite config — https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const emitSourcemaps = mode === 'development'

  return {
    build: {
      sourcemap: emitSourcemaps ? 'inline' : false,
      minify: !emitSourcemaps,
    },
    plugins: [react(), tailwindcss()],
    // These locate their fonts/WASM via `new URL(..., import.meta.url)`, which pre-bundling breaks.
    optimizeDeps: {
      exclude: ['@docx-editor.dev/core', '@docx-editor.dev/fonts'],
    },
    server: {
      host: '0.0.0.0',
      port: parseInt(process.env.PORT || '8443'),
      strictPort: true,
      // The backend (uvicorn on :8000) behind the dev server, same as nginx in Docker: one
      // origin, so the sign-in cookie is first-party. /callback is Authentik's redirect back.
      proxy: Object.fromEntries(
        ['/api', '/plots', '/study-files', '/callback'].map((path) => [path, 'http://localhost:8000']),
      ),
    },
    preview: {
      host: '0.0.0.0',
      port: parseInt(process.env.PORT || '8443'),
    },
  }
})
