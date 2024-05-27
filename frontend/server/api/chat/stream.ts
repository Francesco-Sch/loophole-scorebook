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

	const reader = response.body.getReader();
	const encoder = new TextEncoder();
	const decoder = new TextDecoder();

	const stream = new ReadableStream({
		async start(controller) {
			while (true) {
				const { done, value } = await reader.read();
				if (done) {
					break;
				}

				// Convert the chunk to a string
				const text = decoder.decode(value, { stream: true });

				// Transform the text into a single JSON object
				let eventValue = "";
				let dataValue = "";
				const lines = text.split("\n");
				for (const line of lines) {
					if (line.startsWith("event: ")) {
						eventValue = line.substring(7).trim();
					} else if (line.startsWith("data: ")) {
						dataValue = line.substring(6).trim();
					}
				}

				const jsonObject = {
					event: eventValue,
					data: dataValue.replace(/['"]+/g, ""),
				};

				const jsonChunk = JSON.stringify(jsonObject) + "\n\n";

				console.log(jsonChunk);

				// Enqueue the transformed chunk
				controller.enqueue(encoder.encode(jsonChunk));
			}
			controller.close();
		},
	});

	return sendStream(event, stream);
});
