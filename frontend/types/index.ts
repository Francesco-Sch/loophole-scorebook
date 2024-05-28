declare global {
	interface File {
		filepath: string;
		mimetype: string;
		mtime: string;
		newFilename: string;
		originalFilename: string;
		size: number;
		analyzing?: boolean;
	}
}

export {};
