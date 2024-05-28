import fs from "node:fs";

export default defineEventHandler(async (event) => {
	try {
		// Read the request body
		const body = await readBody(event);

		// Get the list of files from the specified directory
		const files = fs.readdirSync("/tmp/files");

		// Find the file that matches the newFilename provided in the body
		const file = files.find((f) => f === body.file.newFilename);

		// If the file is not found, return an error response
		if (!file) {
			return { success: false, message: "File not found" };
		}

		// Construct the file path
		const filePath = `/tmp/files/${file}`;

		const fileData = fs.readFileSync(filePath);
		const blob = new Blob([fileData], { type: "application/pdf" });

		// Create a new FormData instance
		const formData = new FormData();

		// Append the file stream to the FormData instance
		formData.append("file", blob, body.file.newFilename);

		// Perform the fetch request to the backend
		const response = await $fetch("http://backend:8080/database/post", {
			method: "POST",
			body: formData,
		});

		// Log the response from the backend
		console.log(response);

		// Return a success response
		return {
			success: true,
			message: "File embedded successfully",
			response: response,
		};
	} catch (error) {
		// Log any errors that occur
		console.error(error);

		// Return an error response
		return { success: false, message: error };
	}
});
