// Copyright (c) 2026, AgriTheory and contributors
// For license information, please see license.txt

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path, { resolve } from 'path'
import { existsSync, readFileSync, writeFileSync } from 'fs'

function frappeAssetsPlugin() {
	return {
		name: 'frappe-assets',
		writeBundle(_, bundle) {
			const sitesDir = resolve(__dirname, '../../../../../sites')
			const assetsJsonPath = resolve(sitesDir, 'assets', 'assets.json')
			if (existsSync(assetsJsonPath)) {
				const assetsJson = JSON.parse(readFileSync(assetsJsonPath, 'utf-8'))
				for (const [filename, chunk] of Object.entries(bundle)) {
					if (chunk.type === 'chunk' && chunk.isEntry) {
						assetsJson[`${chunk.name}.bundle.js`] = `/assets/check_run/dist/js/${filename}`
					}
				}
				writeFileSync(assetsJsonPath, JSON.stringify(assetsJson, null, 4))
				console.log('Updated assets.json with new bundle paths')
			}
		},
	}
}

export default defineConfig({
	plugins: [vue(), frappeAssetsPlugin()],
	build: {
		rollupOptions: {
			input: {
				main: path.resolve(__dirname, './check_run/check_run.js'),
			},
			output: {
				entryFileNames: '[name].[hash].js',
				format: 'iife',
			},
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
