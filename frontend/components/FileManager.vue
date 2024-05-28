<script setup lang="ts">
import { storeToRefs } from "pinia";
const defaultStore = useDefaultStore();

const { files } = storeToRefs(defaultStore);
const analyzing = computed(() => {
	return files.value.some((file) => file.analyzing);
});

function removeFile(newFilename) {
	console.log("Removing file", newFilename);
	defaultStore.removeFile(newFilename);
}
</script>

<template>
	<Accordion label="Rulesets" :processing="analyzing" class="mt-auto">
		<FileListItem
			v-for="file in files"
			:key="file.filepath"
			:name="file.originalFilename"
			:analyzing="file.analyzing"
			@remove="removeFile(file.newFilename)"
		/>
	</Accordion>
</template>

<style scoped></style>
