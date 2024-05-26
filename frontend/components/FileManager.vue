<script setup lang="ts">
const defaultStore = useDefaultStore();

const files = defaultStore.getFiles;
</script>

<template>
	<Accordion label="Rulesets" :processing="true">
		<FileListItem
			v-for="file in files"
			:key="file.id"
			:name="file.name"
			:processing="file.processing"
		/>
	</Accordion>
</template>

<style scoped></style>
