<script setup lang="ts">
async function uploadFile(event: Event) {
	const target = event.target as HTMLInputElement;
	const files = target.files;

	if (!files || files.length === 0) {
		return;
	}

	const formData = new FormData();
	for (let i = 0; i < files.length; i++) {
		formData.append("files", files[i]);
	}

	// Send the files to the backend
	try {
		const response = await $fetch("/api/upload/pdf", {
			method: "POST",
			body: formData,
		});

		console.log(response);
	} catch (error) {
		console.error(error);
	}
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
				multiple="true"
				class="w-0 overflow-hidden"
			/>
			Choose a file
		</label>
	</div>
</template>

<style scoped></style>
