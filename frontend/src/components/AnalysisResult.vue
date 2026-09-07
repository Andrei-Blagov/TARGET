<script setup>
import { Motion } from 'motion-v'
import FinalAnalysisCards from './FinalAnalysisCards.vue'

defineProps({
  result: {
    type: Object,
    required: true,
  },
})
</script>

<template>
  <div class="space-y-8">
    <Motion
      as="section"
      class="rounded-2xl border border-line bg-card p-5 shadow-sm"
      :initial="{ opacity: 0, y: 18 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ duration: 0.4 }"
    >
      <p class="text-xs font-semibold uppercase tracking-wide text-accent">Сайт</p>
      <a
        :href="result.url"
        target="_blank"
        rel="noopener noreferrer"
        class="mt-1 break-all text-base font-medium text-ink underline-offset-2 hover:underline"
      >
        {{ result.url }}
      </a>
    </Motion>

    <Motion
      v-if="result.steps?.length"
      as="section"
      class="space-y-3"
      :initial="{ opacity: 0, y: 18 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ delay: 0.08, duration: 0.4 }"
    >
      <h2 class="text-xl font-semibold text-ink sm:text-2xl">Шаги анализа</h2>
      <ol class="space-y-2">
        <Motion
          v-for="(step, index) in result.steps"
          :key="index"
          as="li"
          class="rounded-xl border border-line bg-card px-4 py-3 text-sm leading-relaxed text-muted shadow-sm"
          :initial="{ opacity: 0, x: -12 }"
          :animate="{ opacity: 1, x: 0 }"
          :transition="{ delay: 0.1 + index * 0.05, duration: 0.35 }"
        >
          <span class="mr-2 font-semibold text-accent">{{ index + 1 }}.</span>
          {{ step }}
        </Motion>
      </ol>
    </Motion>

    <Motion
      v-if="result.intermediate_results?.length"
      as="section"
      class="space-y-3"
      :initial="{ opacity: 0, y: 18 }"
      :animate="{ opacity: 1, y: 0 }"
      :transition="{ delay: 0.12, duration: 0.4 }"
    >
      <h2 class="text-xl font-semibold text-ink sm:text-2xl">Промежуточные результаты</h2>
      <div class="space-y-3">
        <details
          v-for="(item, index) in result.intermediate_results"
          :key="index"
          class="rounded-xl border border-line bg-card p-4 shadow-sm"
        >
          <summary class="cursor-pointer text-sm font-medium text-ink">
            Шаг {{ index + 1 }}: {{ item.step }}
          </summary>
          <p class="mt-3 whitespace-pre-wrap text-sm leading-relaxed text-muted">
            {{ item.result }}
          </p>
        </details>
      </div>
    </Motion>

    <FinalAnalysisCards
      v-if="result.final_analysis"
      :analysis="result.final_analysis"
    />
  </div>
</template>
