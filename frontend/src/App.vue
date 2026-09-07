<script setup>
import { ref } from 'vue'
import { Motion } from 'motion-v'
import { analyzeSite, getErrorMessage } from './api'
import Loader from './components/Loader.vue'
import AnalysisResult from './components/AnalysisResult.vue'

const url = ref('')
const loading = ref(false)
const error = ref('')
const result = ref(null)

async function onSubmit() {
  error.value = ''
  result.value = null

  const trimmed = url.value.trim()
  if (!trimmed) {
    error.value = 'Введите ссылку на сайт'
    return
  }

  loading.value = true
  try {
    result.value = await analyzeSite(trimmed)
  } catch (err) {
    error.value = getErrorMessage(err)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen px-4 py-10 sm:px-6 sm:py-14">
    <main class="mx-auto w-full max-w-[800px]">
      <Motion
        as="header"
        class="mb-8 text-center sm:mb-10"
        :initial="{ opacity: 0, y: -16 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ duration: 0.5 }"
      >
        <p class="mb-2 text-xs font-semibold uppercase tracking-[0.18em] text-accent">
          Target AI
        </p>
        <h1 class="text-3xl font-bold leading-tight text-ink sm:text-5xl">
          Анализ сайта для рекламы
        </h1>
        <p class="mt-3 text-sm text-muted sm:text-base">
          Вставьте ссылку — получите шаги, инсайты и примеры постов
        </p>
      </Motion>

      <Motion
        as="form"
        class="rounded-2xl border border-line bg-card p-4 shadow-sm sm:p-5"
        :initial="{ opacity: 0, y: 16 }"
        :animate="{ opacity: 1, y: 0 }"
        :transition="{ delay: 0.1, duration: 0.45 }"
        @submit.prevent="onSubmit"
      >
        <label class="mb-2 block text-sm font-medium text-ink" for="site-url">
          Ссылка на сайт
        </label>
        <div class="flex flex-col gap-3 sm:flex-row">
          <input
            id="site-url"
            v-model="url"
            type="url"
            placeholder="https://example.com"
            class="w-full rounded-xl border border-line bg-surface px-4 py-3 text-sm text-ink outline-none transition placeholder:text-muted/70 focus:border-accent"
            :disabled="loading"
            required
          />
          <button
            type="submit"
            class="rounded-xl bg-accent px-5 py-3 text-sm font-semibold text-white transition hover:bg-accent-dark disabled:cursor-not-allowed disabled:opacity-60 sm:min-w-36"
            :disabled="loading"
          >
            Отправить
          </button>
        </div>

        <Motion
          v-if="error"
          as="p"
          class="mt-3 rounded-xl border border-danger/20 bg-danger/5 px-3 py-2 text-sm text-danger"
          :initial="{ opacity: 0, y: 6 }"
          :animate="{ opacity: 1, y: 0 }"
          role="alert"
        >
          {{ error }}
        </Motion>
      </Motion>

      <div v-if="result" class="mt-8">
        <AnalysisResult :result="result" />
      </div>
    </main>

    <Loader v-if="loading" />
  </div>
</template>
