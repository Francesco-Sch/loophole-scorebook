<script setup>
function handleFiles(event) {
	console.log(event);
}
</script>

<template>
	<div class="flex justify-center items-center w-full flex-1">
		<FileUpload @success="handleFiles" />
	</div>
</template>

<style scoped></style>
