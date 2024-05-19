// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
	devtools: { enabled: true },
	googleFonts: {
		families: {
			"Jacquard 12": true,
		},
	},
	modules: ["@nuxtjs/tailwindcss", "@nuxtjs/google-fonts", "@vueuse/nuxt"],
});
