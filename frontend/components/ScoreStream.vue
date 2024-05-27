<script setup lang="ts">
import { ref, onMounted } from "vue";

const prompt = ref<string>("What do you think of the new ruleset?");
const score = ref<string>("");

async function fetchScore(prompt: string) {
	const response = await fetch("/api/chat/stream", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ prompt }),
	});

	const reader = response.body.getReader();
	const decoder = new TextDecoder("utf-8");
	let currentEvent = "";

	const read = async () => {
		const { done, value } = await reader.read();
		if (done) {
			console.log("release locked");
			return reader.releaseLock();
		}

		const chunk = decoder.decode(value, { stream: true });

		// Parse the chunk and append to score if the event is 'data'
		const lines = chunk.split("\n");
		for (const line of lines) {
			if (line.startsWith("event: ")) {
				currentEvent = line.slice("event: ".length).trim();
			} else if (line.startsWith("data: ")) {
				let data = line.slice("data: ".length).trim();
				if (currentEvent === "data") {
					// Remove quotation marks and handle newlines
					data = data.replace(/^"|"$/g, "").replace(/\\n/g, "\n");
					score.value += data;
				}
			}
		}

		console.log(chunk);

		return read();
	};
	await read();
}

onMounted(() => {
	fetchScore(prompt.value);
});
</script>

<template>
	<div>
		<p v-html="score"></p>
		<UButton @click="fetchScore(prompt.value)">Next score</UButton>
	</div>
</template>

<style scoped></style>
