<script setup lang="ts">
// State
const uploadSuccess = ref<boolean>(false);
const uploadError = ref<boolean>(false);

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

		// Clear the input field
		target.value = "";

		// Trigger a success or error message
		// @ts-ignore
		if (response.success === true) {
			uploadSuccess.value = true;

			// Wait for 3 seconds and then hide the success message
			setTimeout(() => {
				uploadSuccess.value = false;
			}, 3000);
		} else {
			uploadError.value = true;

			// Wait for 3 seconds and then hide the error message
			setTimeout(() => {
				uploadError.value = false;
			}, 3000);
		}
	} catch (error) {
		console.error(error);
	}
}
</script>

<template>
	<div
		class="flex flex-col justify-center items-center w-max p-12 border-2 border-black border-dotted relative"
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

		<!-- Success Message -->
		<Transition name="status">
			<div
				class="bg-black absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center"
				v-if="uploadSuccess"
			>
				<Icon name="octicon:check-circle-fill-16" color="white" size="20px" />
				<p class="text-white mt-4">Upload successful</p>
			</div>
		</Transition>

		<!-- Error Message -->
		<Transition name="status">
			<div
				class="bg-black absolute top-0 left-0 w-full h-full flex flex-col items-center justify-center"
				v-if="uploadError"
			>
				<Icon name="octicon:alert-16" color="white" size="20px" />
				<p class="text-white mt-4">Upload failed</p>
			</div>
		</Transition>
	</div>
</template>

<style scoped>
.status-enter-active {
	animation: slide-up 0.5s ease-out;
}
.status-leave-active {
	animation: slide-up 0.5s ease-out reverse;
}
@keyframes slide-up {
	0% {
		opacity: 0;
		transform: translateY(5%);
	}
	20% {
		opacity: 0.7;
	}
	100% {
		opacity: 1;
		transform: translateY(0%);
	}
}
</style>
