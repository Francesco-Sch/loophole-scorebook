import { readFiles } from "h3-formidable";
import fs from "fs";

export default defineEventHandler(async (event) => {
	// Create upload directory
	if (!fs.existsSync("/tmp/files")) {
		fs.mkdir("/tmp/files", { recursive: true }, (err) => {
			if (err) {
				console.error("Error creating upload directory", err);
			}
		});
	}

	const { fields, files, form } = await readFiles(event, {
		uploadDir: "/tmp/files", // Directory to save uploaded files
		multiples: true, // Enable multiple file uploads
	});

	let uploadedFiles = files.files;

	// Check if there are no files
	if (!uploadedFiles || uploadedFiles.length === 0) {
		return { success: false, message: "No files uploaded" };
	}

	// Ensure uploadedFiles is an array
	if (!Array.isArray(uploadedFiles)) {
		uploadedFiles = [uploadedFiles];
	}

	// Validate files
	const invalidFiles = uploadedFiles.filter(
		(file) => file.mimetype !== "application/pdf"
	);
	if (invalidFiles.length > 0) {
		return {
			success: false,
			message: "One or more files are not PDFs",
			invalidFiles,
		};
	}

	return { success: true, message: "Files uploaded", files: uploadedFiles };
});
