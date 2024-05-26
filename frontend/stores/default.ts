export const useDefaultStore = defineStore("defaultStore", {
	state: () => ({
		files: [],
	}),
	getters: {
		getFiles: (state) => state.files,
	},
});
