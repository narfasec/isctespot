<script setup>
import { computed, useSlots } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: null
  },
  labelFor: {
    type: String,
    default: null
  },
  help: {
    type: String,
    default: null
  },
  size: {
    type: String,
    default: 'normal', // Default to 'normal' if not specified
    validator: value => ['small', 'normal'].includes(value) // Only allow 'small' or 'normal'
  }
})

const slots = useSlots()

const wrapperClass = computed(() => {
  const base = []
  const slotsLength = slots.default().length

  if (slotsLength > 1) {
    base.push('grid grid-cols-1 gap-3')
  }

  if (slotsLength === 2) {
    base.push('md:grid-cols-2')
  }

  // Adjust classes if size is small
  if (props.size === 'small') {
    base.push('text-sm py-1') // Example classes for smaller size
  }

  return base
})
</script>

<template>
  <div :class="[props.size === 'small' ? 'mb-3' : 'mb-6', 'last:mb-0']">
    <label v-if="label" :for="labelFor" :class="size === 'small' ? 'text-sm' : 'block font-bold mb-2'">
      {{ label }}
    </label>
    <div :class="wrapperClass">
      <slot />
    </div>
    <div v-if="help" :class="['text-xs', size === 'small' ? 'mt-0.5' : 'mt-1', 'text-gray-500 dark:text-slate-400']">
      {{ help }}
    </div>
  </div>
</template>
