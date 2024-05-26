import fs from "fs";
import FormData from "form-data";

export default defineEventHandler(async (event) => {
	const body = await readBody(event);
	const formData = new FormData();

	const files = fs.readdirSync("/tmp/files");
	const file = files.find((f) => f === body.file.newFilename);

	if (!file) {
		return { success: false, message: "File not found" };
	}

	const filePath = `/tmp/files/${file}`;

	const stream = fs.createReadStream(filePath);
	formData.append("file", stream);

	const response = await $fetch("http://lhscr-backend:8080/database/post", {
		headers: {
			"Content-Type": "multipart/form-data",
		},
		method: "POST",
		body: formData,
	});

	console.log(response);

	return { success: true, message: "File sent", response: response };
});
