<script setup>
import { computed } from 'vue'
import { Motion } from 'motion-v'

const props = defineProps({
  analysis: {
    type: Object,
    required: true,
  },
})

const entries = computed(() => Object.entries(props.analysis || {}))

function titleFromKey(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

function isExamplesKey(key) {
  return key.toLowerCase().includes('examples')
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}
</script>

<template>
  <section class="space-y-4">
    <h2 class="text-xl font-semibold text-ink sm:text-2xl">Итоговый анализ</h2>

    <Motion
      v-for="([key, value], index) in entries"
      :key="key"
      as="article"
      class="rounded-2xl border border-line bg-card p-5 shadow-sm"
      :initial="{ opacity: 0, y: 24 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ delay: index * 0.08, duration: 0.45 }"
    >
      <h3 class="mb-3 text-sm font-semibold uppercase tracking-wide text-accent">
        {{ titleFromKey(key) }}
      </h3>

      <div v-if="isExamplesKey(key) && Array.isArray(value)" class="grid gap-3">
        <Motion
          v-for="(example, i) in value"
          :key="i"
          as="div"
          class="rounded-xl border border-line bg-surface px-4 py-3 text-sm leading-relaxed text-ink"
          :initial="{ opacity: 0, scale: 0.96 }"
          :animate="{ opacity: 1, scale: 1 }"
          :transition="{ delay: 0.15 + i * 0.08, duration: 0.35 }"
        >
          {{ example }}
        </Motion>
      </div>

      <ul v-else-if="Array.isArray(value)" class="list-disc space-y-2 pl-5 text-sm leading-relaxed text-muted">
        <li v-for="(item, i) in value" :key="i">{{ item }}</li>
      </ul>

      <pre
        v-else-if="isPlainObject(value)"
        class="overflow-x-auto whitespace-pre-wrap break-words rounded-xl bg-surface p-3 text-xs text-muted"
      >{{ JSON.stringify(value, null, 2) }}</pre>

      <p v-else class="whitespace-pre-wrap text-sm leading-relaxed text-muted">
        {{ value }}
      </p>
    </Motion>
  </section>
</template>
