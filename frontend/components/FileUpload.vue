<script setup lang="ts">
function uploadFile(event: Event) {
	const target = event.target as HTMLInputElement;
	const file = target.files?.[0];
	if (!file) return;

	const formData = new FormData();
	formData.append("file", file);

	fetch("/api/upload", {
		method: "POST",
		body: formData,
	})
		.then((response) => response.json())
		.then((data) => console.log(data))
		.catch((error) => console.error(error));
}
</script>

<template>
	<div
		class="flex flex-col justify-center items-center w-max p-12 border-2 border-black border-dotted"
	>
		<p class="text-neutral-400 mb-4">Upload your ruleset</p>
		<label
			class="p-2 border border-black rounded bg-black text-white hover:cursor-pointer"
		>
			<input
				type="file"
				@change="uploadFile"
				accept=".pdf"
				class="w-0 overflow-hidden"
			/>
			Choose a file
		</label>
	</div>
</template>

<style scoped></style>
