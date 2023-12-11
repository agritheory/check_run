import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'
import { getProxyOptions } from 'frappe-ui/src/utils/vite-dev-server'
// import { webserver_port } from '../../../../sites/common_site_config.json'

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8080,
		proxy: getProxyOptions({ port: 8003 }),
	},
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
