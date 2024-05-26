// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	devtools: { enabled: true },
	googleFonts: {
		families: {
			"Jacquard 12": true,
			"Xanh Mono": true,
		},
	},
	modules: [
		"@nuxt/ui",
		"@nuxtjs/google-fonts",
		"@vueuse/nuxt",
		"@pinia/nuxt",
		"nuxt-icon",
	],
	ui: {
		icons: ["octicon"],
	},
});
