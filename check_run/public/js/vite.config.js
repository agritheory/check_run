import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	build: {
		outDir: './check_run/public',
		emptyOutDir: false,
		manifest: false,
		rollupOptions: {
			input: {
				check_run: path.resolve(__dirname, './check_run/check_run.js'),
			},
			output: {
				entryFileNames: 'js/check_run_vue.bundle.js',
				assetFileNames: 'assets/[name].[ext]',
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
