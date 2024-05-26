import { readFiles } from "h3-formidable";

export default defineEventHandler(async (event) => {
	const { fields, files, form } = await readFiles(event, {
		multiples: true, // Enable multiple file uploads
	});

	let uploadedFiles = files.files; // This will be an array if multiple files are uploaded

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
