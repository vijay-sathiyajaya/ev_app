<template>
  <div id="app" class="container">
    <h1>{{ title }}</h1>
    <p>Welcome to your Vue 3 + Vite application</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const title = ref('Frontend Application')
</script>

<style scoped>
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}
</style>
