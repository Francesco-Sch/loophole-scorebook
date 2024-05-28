<script setup lang="ts">
import { sleep } from "../utils/sleep";

const prompt = ref<string>(
	"Give me an score for a provocative art piece or performance I could do, that exploits the rules from the ruleset provided in the context."
);
const score = ref<string>("");

const streaming = ref<boolean>(false);

async function fetchScore(prompt: string) {
	// Clear the score
	score.value = "";

	// Show the cursor
	streaming.value = true;

	// Fetch the score
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

					console.log("Received JSON:", json);

					// Replace \\n in json.data with \n
					if (json.data) {
						json.data = json.data.replace(/\\n/g, "\n");
					}

					if (json.event === "data") {
						score.value += json.data;
					}

					if (json.event === "end") {
						streaming.value = false;
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
	sleep(500);
	fetchScore(prompt.value);
});
</script>

<template>
	<div class="w-1/2 max-h-[70%] flex flex-col overflow-hidden my-auto">
		<pre
			class="text-lg whitespace-pre-wrap overflow-auto flex-grow relative scrollbar">{{ score }}<span class="blinking-cursor ml-1" v-show="streaming"> </span></pre>
		<UButton
			variant="ghost"
			class="text-lg text-black mt-7 p-0 hover:bg-transparent hover:underline"
			icon="i-octicon-arrow-right-24"
			trailing
			@click="fetchScore(prompt.value)"
			>Next score</UButton
		>
	</div>
</template>

<style scoped>
.scrollbar {
	scrollbar-color: #000000 transparent;
	scrollbar-width: thin;
}

.blinking-cursor {
	display: inline-block;
	width: 0.75ch;
	height: 2.5ch;
	background-color: black;
	animation: blink 1s step-end infinite;
}

@keyframes blink {
	0%,
	50% {
		background-color: black;
	}
	50.01%,
	100% {
		background-color: transparent;
	}
}
</style>
