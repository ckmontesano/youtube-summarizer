<script setup>
import VideoSummarizer from './components/VideoSummarizer.vue'
</script>

<template>
  <VideoSummarizer />
</template>
<style>
:root {
  --primary-color: #2563eb;
  --background-color: #f8fafc;
  --text-color: #1e293b;
  --border-color: #e2e8f0;
  --error-color: #dc2626;
  --card-background: #ffffff;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

@media (prefers-color-scheme: dark) {
  :root {
    --background-color: #0f172a;
    --text-color: #f1f5f9;
    --border-color: #334155;
    --card-background: #1e293b;
  }
}
</style>

