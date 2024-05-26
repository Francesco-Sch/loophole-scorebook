export const useDefaultStore = defineStore("defaultStore", {
	state: () => ({
		files: [],
	}),
	getters: {
		getFiles: (state) => state.files,
	},
	actions: {
		setFiles(files) {
			this.files = files;
		},
		addFiles(files) {
			this.files.push(...files);
		},
		removeFile(filename) {
			this.files = this.files.filter(
				({ newFilename }) => newFilename !== filename
			);
		},
	},
});
