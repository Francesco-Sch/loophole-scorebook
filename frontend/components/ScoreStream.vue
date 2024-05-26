<script setup lang="ts">
const prompt = ref<string>("What do you think of the new ruleset?");

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
	const read = async () => {
		const { done, value } = await reader.read();
		if (done) {
			console.log("release locked");
			return reader.releaseLock();
		}

		const chunk = decoder.decode(value, { stream: true });
		const temp = chunk.replace(/\}/g, "},"); //JSON.parse(JSON.stringify(chunk));
		const jsonData = temp
			.split(",")
			.map((data) => {
				const trimData = data.trim();
				console.log(trimData);
				if (trimData === "") return undefined;
				if (trimData === '{"content":"\n\n"}') return undefined;
				if (trimData === "[DONE]") return undefined;
				return trimData;
			})
			.filter((data) => data);

		var textOutput = "";

		for (let i = 0; i < jsonData.length; i++) {
			try {
				if (JSON.parse(jsonData[i]).content === "\n\n") {
					textOutput = "";
				} else {
					textOutput = JSON.parse(jsonData[i]);
				}
			} catch (e) {
				console.log(e);
			}

			if (textOutput.content !== undefined) {
				generateText.value = generateText.value + textOutput.content;
			}
		}
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
		<p></p>
		<UButton>Next score</UButton>
	</div>
</template>

<style scoped></style>
