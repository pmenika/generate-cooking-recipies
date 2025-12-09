<template>
<div>Hi</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';

const recipe = ref('')
const getRecipe = async() => {
  try {
    const response = await fetch('http://localhost:8000/api/ai-chat');
    recipe.value = await response.json();
  } catch (error) {
    console.error('Error fetching recipe:', error);
  }
}

onMounted(() => {
  getRecipe();
});
</script>
