<script setup lang="ts">
import { storeToRefs } from "pinia";

const defaultStore = useDefaultStore();

let chat = ref<boolean>(false);

function addFilesToStore(event) {
	defaultStore.setFiles(event.files);

	console.log("Files added to store");
}

async function embedFile(file) {
	const response = await $fetch("/api/embed/pdf", {
		method: "POST",
		body: JSON.stringify({ file }),
		headers: {
			"Content-Type": "application/json",
		},
	});

	console.log(response);
}

watch(
	() => defaultStore.getFiles,
	(files) => {
		if (files.length > 0) {
			files.forEach((file) => {
				embedFile(file);
			});
		}
	}
);
</script>

<template>
	<div class="flex flex-col justify-center items-center w-full flex-1">
		<FileUpload
			@success="addFilesToStore"
			v-if="defaultStore.getFiles.length === 0"
		/>
		<template v-else-if="chat">
			<ScoreStream />
			<FileManager />
		</template>
		<template v-else>
			<p class="my-auto text-neutral-400 text-3xl">
				<span class="mx-4">Analyzing the ruleset...</span>
			</p>
			<FileManager />
		</template>
	</div>
</template>

<style scoped></style>
