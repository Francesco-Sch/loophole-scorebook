<script setup lang="ts">
const props = defineProps({
	label: String,
	processing: Boolean,
});

const isOpen = ref<boolean>(false);

function toggle() {
	isOpen.value = !isOpen.value;
}
</script>

<template>
	<div class="min-w-[10%] w-[15%] p-3 bg-black text-white">
		<div class="flex justify-start items-center cursor-pointer" @click="toggle">
			<span class="flex-1">{{ label }}</span>
			<span v-if="processing">
				<Icon
					name="svg-spinners:pulse-3"
					class="text-emerald-400"
					size="20px"
				/>
			</span>
			<span
				:class="{ 'transform rotate-180': isOpen }"
				class="transition-transform duration-200"
			>
				<Icon name="octicon:chevron-up" size="20px" class="mx-1" />
			</span>
		</div>
		<div v-show="isOpen" class="mt-4">
			<!-- Content to be shown when expanded -->
			<slot />
		</div>
	</div>
</template>
