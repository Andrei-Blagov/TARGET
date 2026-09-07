<script setup>
import { Motion } from 'motion-v'
</script>

<template>
  <Motion
    as="div"
    class="fixed inset-0 z-50 flex items-center justify-center bg-[rgba(18,32,46,0.45)] px-4 backdrop-blur-sm"
    :initial="{ opacity: 0 }"
    :animate="{ opacity: 1 }"
    :transition="{ duration: 0.25 }"
  >
    <Motion
      as="div"
      class="flex w-full max-w-sm flex-col items-center gap-4 rounded-2xl bg-card px-6 py-8 text-center shadow-lg"
      :initial="{ scale: 0.94, opacity: 0 }"
      :animate="{ scale: 1, opacity: 1 }"
      :transition="{ duration: 0.3 }"
    >
      <div
        class="h-12 w-12 animate-spin rounded-full border-4 border-line border-t-accent"
        aria-hidden="true"
      />
      <p class="text-base font-medium text-ink">Анализируем сайт...</p>
      <p class="text-sm text-muted">Это может занять пару минут</p>
    </Motion>
  </Motion>
</template>
