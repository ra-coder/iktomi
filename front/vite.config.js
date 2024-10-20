import { defineConfig } from 'vite';

export default defineConfig({
  build: {
    outDir: 'dist',          // Output directory
  },
  resolve: {
    alias: {
      '@reown/appkit': '/node_modules/@reown/appkit', // Resolve alias for browser
    },
  },
});