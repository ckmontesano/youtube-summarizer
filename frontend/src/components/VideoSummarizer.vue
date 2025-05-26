<template>
  <div class="app">
    <div class="container">
      <header>
        <h1>YouTube Video Summarizer</h1>
        <p>Enter a YouTube video URL to get an AI-generated summary</p>
      </header>

      <main>
        <form @submit.prevent="handleSubmit" class="search-form">
          <div class="form-group">
            <input
              v-model="videoUrl"
              type="url"
              placeholder="https://www.youtube.com/watch?v=..."
              :disabled="isLoading"
              required
            />
            <button type="submit" :disabled="isLoading || !videoUrl">
              {{ isLoading ? 'Processing...' : 'Summarize' }}
            </button>
          </div>
        </form>

        <div v-if="isLoading" class="loading">
          <div class="spinner"></div>
          <p>Generating summary...</p>
        </div>

        <div v-if="error" class="error">
          <p>{{ error }}</p>
        </div>

        <!-- Current summary -->
        <div v-if="currentSummary" class="summary current">
          <div class="summary-header">
            <h2>Latest Summary</h2>
            <span class="timestamp">{{ formatDate(currentSummary.timestamp) }}</span>
          </div>
          <div class="summary-content" v-html="formatSummary(currentSummary.summary)"></div>
          <div class="summary-meta">
            <a :href="currentSummary.url" target="_blank" rel="noopener" class="video-link">
              View Video
            </a>
          </div>
        </div>

        <!-- History -->
        <div v-if="history.length > 0" class="history">
          <h2>Previous Summaries</h2>
          <div class="accordion">
            <div v-for="(item, index) in history" :key="item.timestamp" class="accordion-item">
              <button 
                class="accordion-header"
                @click="toggleAccordion(index)"
                :aria-expanded="openAccordion === index"
              >
                <div class="header-content">
                  <span class="video-title">{{ item.title }}</span>
                  <span class="timestamp">{{ formatDate(item.timestamp) }}</span>
                </div>
                <span class="toggle-icon">{{ openAccordion === index ? '−' : '+' }}</span>
              </button>
              <div 
                v-show="openAccordion === index"
                class="accordion-content"
              >
                <div class="summary-content" v-html="formatSummary(item.summary)"></div>
                <div class="summary-meta">
                  <a :href="item.url" target="_blank" rel="noopener" class="video-link">
                    View Video
                  </a>
                  <button @click="deleteHistoryItem(index)" class="delete-btn">
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </main>

      <footer>
        <p>Powered by OpenAI GPT-3.5</p>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const videoUrl = ref('')
const error = ref('')
const isLoading = ref(false)
const openAccordion = ref(null)
const history = ref([])
const currentSummary = ref(null)

// Load history from localStorage on mount
onMounted(() => {
  const savedHistory = localStorage.getItem('summaryHistory')
  if (savedHistory) {
    const parsed = JSON.parse(savedHistory)
    history.value = parsed.history || []
    currentSummary.value = parsed.current || null
  }
})

// Save history to localStorage whenever it changes
const saveHistory = () => {
  localStorage.setItem('summaryHistory', JSON.stringify({
    history: history.value,
    current: currentSummary.value
  }))
}

const formatSummary = (text) => {
  if (!text) return ''
  
  return text.split('\n\n').map(paragraph => {
    if (paragraph.includes('• ')) {
      return paragraph.split('\n').map(line => `<p>${line}</p>`).join('')
    }
    return `<p>${paragraph}</p>`
  }).join('')
}

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

const toggleAccordion = (index) => {
  openAccordion.value = openAccordion.value === index ? null : index
}

const deleteHistoryItem = (index) => {
  history.value.splice(index, 1)
  saveHistory()
  if (openAccordion.value === index) {
    openAccordion.value = null
  } else if (openAccordion.value > index) {
    openAccordion.value--
  }
}

const handleSubmit = async () => {
  error.value = ''
  isLoading.value = true

  try {
    const response = await axios.post('http://localhost:3000/api/summarize', {
      videoUrl: videoUrl.value
    })
    
    const newSummary = {
      url: videoUrl.value,
      title: response.data.title.replace(/^"|"$/g, ''),  // Remove quotes when storing the title
      summary: response.data.summary,
      timestamp: Date.now()
    }

    // Add to history
    history.value.unshift(newSummary)
    // Keep only last 10 items
    if (history.value.length > 10) {
      history.value.pop()
    }

    // Set as current summary
    currentSummary.value = newSummary
    videoUrl.value = ''
    
    // Save to localStorage
    saveHistory()
  } catch (err) {
    error.value = err.response?.data?.error || 'Failed to generate summary'
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: white;
  color: #333;
}

.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
}

header {
  text-align: center;
  margin-bottom: 3rem;
}

h1 {
  font-size: 2.5rem;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

header p {
  color: #666;
  font-size: 1.1rem;
}

.search-form {
  margin-bottom: 2rem;
}

.form-group {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

input[type="url"] {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  font-size: 1rem;
  background: white;
  transition: border-color 0.2s;
}

input[type="url"]:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.1);
}

input[type="url"]:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

button {
  padding: 0.75rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover:not(:disabled) {
  background: #1d4ed8;
}

button:disabled {
  background: #93c5fd;
  cursor: not-allowed;
}

.loading {
  text-align: center;
  margin: 2rem 0;
  color: #666;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 1rem;
  border: 3px solid #f3f4f6;
  border-top-color: #2563eb;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error {
  padding: 1rem;
  background: #fee2e2;
  border: 1px solid #ef4444;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}

.error p {
  color: #dc2626;
}

.summary {
  background: white;
  padding: 2rem;
  border-radius: 0.5rem;
  border: 1px solid #e5e7eb;
  margin-bottom: 2rem;
}

.summary.current {
  background: #f8fafc;
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.summary h2 {
  color: #1a1a1a;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.summary-content {
  white-space: pre-line;
  line-height: 1.6;
}

.summary-content :deep(p) {
  margin-bottom: 1rem;
  color: #374151;
}

.summary-content :deep(p:last-child) {
  margin-bottom: 0;
}

.summary-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.video-link {
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.video-link:hover {
  color: #1d4ed8;
  text-decoration: underline;
}

.timestamp {
  color: #6b7280;
  font-size: 0.875rem;
}

.history {
  margin-top: 3rem;
}

.history h2 {
  color: #1a1a1a;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
}

.accordion {
  border: 1px solid #e5e7eb;
  border-radius: 0.5rem;
  overflow: hidden;
}

.accordion-item {
  border-bottom: 1px solid #e5e7eb;
}

.accordion-item:last-child {
  border-bottom: none;
}

.accordion-header {
  width: 100%;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f9fafb;
  border: none;
  cursor: pointer;
  text-align: left;
  font-size: 1rem;
  color: #1a1a1a;
  transition: background-color 0.2s;
}

.accordion-header:hover {
  background: #f3f4f6 !important;  /* Override button hover styles */
}

.header-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.video-title {
  font-weight: 500;
  color: #1a1a1a;
}

.toggle-icon {
  font-size: 1.25rem;
  color: #9ca3af;
  width: 1.5rem;
  text-align: center;
  transition: transform 0.2s;
}

.accordion-content {
  padding: 1.25rem;
  background: white;
  border-top: 1px solid #f3f4f6;
}

.delete-btn {
  padding: 0.5rem 0.75rem;
  background: #f8fafc;
  color: #6b7280;
  border: 1px solid #e5e7eb;
  border-radius: 0.375rem;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #f1f5f9;
  color: #dc2626;
  border-color: #fecaca;
}

footer {
  text-align: center;
  padding: 2rem 0;
  color: #6b7280;
  font-size: 0.875rem;
  border-top: 1px solid #f3f4f6;
  margin-top: 2rem;
}

@media (max-width: 640px) {
  .container {
    padding: 1.5rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .form-group {
    flex-direction: column;
  }
  
  button {
    width: 100%;
  }

  .accordion-header {
    padding: 0.875rem 1rem;
  }

  .header-content {
    gap: 0.125rem;
  }
  
  .video-title {
    font-size: 0.9375rem;
  }
  
  .timestamp {
    font-size: 0.75rem;
  }

  .accordion-content {
    padding: 1rem;
  }

  .summary {
    padding: 1.5rem;
  }
}
</style> 