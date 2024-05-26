<script setup lang="ts">
const defaultStore = useDefaultStore();

function addFilesToStore(event) {
	defaultStore.setFiles(event.files);

	console.log("Files added to store");
}
</script>

<template>
	<div class="flex flex-col justify-center items-center w-full flex-1">
		<FileUpload
			@success="addFilesToStore"
			v-if="defaultStore.getFiles.length === 0"
		/>
		<template v-else>
			<p class="my-auto text-neutral-400 text-3xl">
				<span class="mx-4">Analyzing the ruleset...</span>
			</p>
			<FileManager />
		</template>
	</div>
</template>

<style scoped></style>
