import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	build: {
		outDir: './check_run/public/dist/js',
		emptyOutDir: false,
		manifest: true,
		rollupOptions: {
			input: {
				'check_run': path.resolve(__dirname, './check_run/check_run.js'),
			},
			output: {
				entryFileNames: 'check_run_vue.bundle.[hash].js',
				assetFileNames: 'style.css',
				format: 'iife',
			},
		},
		minify: false,
	},
	optimizeDeps: {},
	define: {
		'process.env': process.env,
	},
})
