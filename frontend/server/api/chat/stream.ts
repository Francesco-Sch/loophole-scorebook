import { sendStream } from "h3";

export default defineEventHandler(async (event) => {
	const body = await readBody(event);
	const prompt = body.prompt;

	const response = await fetch("http://backend:8080/chat/stream", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ input: { prompt: prompt } }),
	});

	if (response.body) {
		return response.body;
	} else {
		return new Response("No data received from backend", { status: 502 });
	}
});
