import { defineConfig } from 'vite'
import react, { reactCompilerPreset } from '@vitejs/plugin-react'
import cesium from 'vite-plugin-cesium'
import babel from '@rolldown/plugin-babel'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    cesium(),
    babel({ presets: [reactCompilerPreset()] })
  ],
})
