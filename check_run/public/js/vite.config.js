import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	build: {
		lib: {
			entry: path.resolve(__dirname, './check_run/check_run.js'),
			name: 'check_run',
			fileName: format => `check_run.js`, // creates module only output
		},
		outDir: './check_run/public/dist/js',
		root: './',
		target: 'es2015',
		emptyOutDir: false,
		minify: false,
	},
	optimizeDeps: {},
	define: {
		'process.env': process.env,
	},
})
