import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	build: {
		outDir: './check_run/public/',
		emptyOutDir: false,
		rollupOptions: {
			input: {
				'check_run': path.resolve(__dirname, './check_run/check_run.js'),
			},
			output: {
				entryFileNames: 'js/compiled/[name].js', // No hash
				assetFileNames: 'dist/js/style.css',
			},
		},
		minify: false,
	},
	optimizeDeps: {},
	define: {
		'process.env': process.env,
	},
})
