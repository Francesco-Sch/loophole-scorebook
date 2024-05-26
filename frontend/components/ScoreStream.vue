<script setup lang="ts">
const prompt = ref<string>("What do you think of the new ruleset?");

async function fetchScore(prompt: string) {
	const response = await $fetch("/api/chat/stream", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ prompt }),
	});

	// Consume stream
	const reader = response.body?.getReader();

	if (!reader) {
		console.error("Failed to get reader");
		return;
	}

	while (true) {
		const { done, value } = await reader.read();

		if (done) {
			console.log("Stream finished");
			break;
		}

		console.log(value);
	}
}

onMounted(() => {
	fetchScore(prompt.value);
});
</script>

<template>
	<div>
		<p></p>
		<UButton>Next score</UButton>
	</div>
</template>

<style scoped></style>
