<script setup lang="ts">
const props = defineProps({
	name: {
		type: String,
		required: true,
		default: "File",
	},
	processing: {
		type: Boolean,
		default: false,
	},
});
const emits = defineEmits(["remove"]);
</script>

<template>
	<div class="border-b border-white flex items-center justify-start py-2">
		<Icon name="octicon:file-16" color="white" />
		<p
			class="mx-2 flex-1 overflow-hidden whitespace-nowrap inner-shadow relative"
		>
			{{ name }}
		</p>

		<Icon
			v-if="processing"
			name="svg-spinners:pulse-3"
			class="text-emerald-400"
		/>
		<UButton
			icon="i-octicon-x"
			variant="ghost"
			size="sm"
			class="text-white hover:bg-black"
			@click="$emit('remove')"
		/>
	</div>
</template>

<style scoped>
.inner-shadow::before {
	content: "";
	position: absolute;
	top: 0;
	right: 0;
	height: 100%;
	width: 20px;
	pointer-events: none;
	background: linear-gradient(to left, rgba(0, 0, 0, 1), transparent);
}
</style>
