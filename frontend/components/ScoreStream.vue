<script setup lang="ts">
const prompt = ref<string>("What do you think of the new ruleset?");
const score = ref<string>("");

async function fetchScore(prompt: string) {
	// Clear the score
	score.value = "";

	const response = await fetch("/api/chat/stream", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ prompt }),
	});

	const reader = response.body.getReader();
	const decoder = new TextDecoder("utf-8");
	let buffer = "";

	const read = async () => {
		const { done, value } = await reader.read();

		if (done) {
			console.log("Release locked");
			return reader.releaseLock();
		}

		buffer += decoder.decode(value, { stream: true });

		// Split the buffer by newlines
		let parts = buffer.split("\n\n");

		// Process all but the last part (which might be incomplete)
		for (let i = 0; i < parts.length - 1; i++) {
			const jsonStr = parts[i];
			if (jsonStr.trim() !== "") {
				try {
					const json = JSON.parse(jsonStr.trim());

					// Replace \\n in json.data with \n
					if (json.data) {
						json.data = json.data.replace(/\\n/g, "\n");
					}

					if (json.event === "data") {
						score.value += json.data;
					}
				} catch (e) {
					console.error("Error parsing JSON:", e);
				}
			}
		}

		// Keep the last partial part in the buffer
		buffer = parts[parts.length - 1];

		return read();
	};

	await read();
}

onMounted(() => {
	fetchScore(prompt.value);
});
</script>

<template>
	<div class="w-1/2">
		<pre class="text-lg whitespace-pre-wrap">{{ score }}</pre>
		<UButton
			variant="ghost"
			class="text-lg text-black mt-5 p-0 hover:bg-transparent hover:underline"
			icon="i-octicon-arrow-right-24"
			trailing
			@click="fetchScore(prompt.value)"
			>Next score</UButton
		>
	</div>
</template>

<style scoped></style>
