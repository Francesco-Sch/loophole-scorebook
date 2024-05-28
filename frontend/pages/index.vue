<script setup lang="ts">
import { storeToRefs } from "pinia";

const defaultStore = useDefaultStore();
const { files } = storeToRefs(defaultStore);
const analyzing = computed(() => {
	return files.value.some((file) => file.analyzing);
});

function addFilesToStore(event) {
	defaultStore.setFiles(event.files);

	console.log("Files added to store");
}

async function embedFile(file: File) {
	// Set analyzing to true for this file
	file.analyzing = true;

	const response = await $fetch("/api/embed/pdf", {
		method: "POST",
		body: JSON.stringify({ file }),
		headers: {
			"Content-Type": "application/json",
		},
	});

	console.log(response);

	// Set analyzing to false for this file
	file.analyzing = false;
}

watch(
	() => files.value,
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
		<template v-else-if="analyzing">
			<p class="my-auto text-neutral-400 text-3xl">
				<span class="mx-4">Analyzing the ruleset...</span>
			</p>
			<FileManager />
		</template>
		<template v-else>
			<ScoreStream />
			<FileManager />
		</template>
	</div>
</template>

<style scoped></style>
