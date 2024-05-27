<script setup lang="ts">
import { storeToRefs } from "pinia";
const defaultStore = useDefaultStore();

const { files } = storeToRefs(defaultStore);

function removeFile(newFilename) {
	console.log("Removing file", newFilename);
	defaultStore.removeFile(newFilename);
}
</script>

<template>
	<Accordion label="Rulesets" :processing="false" class="mt-auto">
		<FileListItem
			v-for="file in files"
			:key="file.filepath"
			:name="file.originalFilename"
			@remove="removeFile(file.newFilename)"
		/>
	</Accordion>
</template>

<style scoped></style>
