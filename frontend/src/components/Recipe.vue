<template>
<div class="flex flex-col max-w-2xl pt-12 pb-24 mx-auto">
  <div v-if="error" class="text-center text-red-500 text-xl mb-4 p-4">
    {{ error }}
  </div>
  <div v-if="loading">
      <p class="text-center text-white text-2xl">Generating recipe...</p>
  </div>
    <div class="recipe-wrapper overflow-y-auto max-h-[calc(100vh-100px)]" v-if="recipe.name">
      <h2 class="font-bold text-3xl mb-6">{{ recipe.name }}</h2>
      <div>
        <h3 class="font-bold text-xl mb-4">Ingredients</h3>
        <div v-for="(ingredient, index) in recipe.ingredients" :key="index" class="border-2 border-gray-400 p-5">
          <span>{{ ingredient.name }}:</span>
          <span>{{ ingredient.quantity }}</span>
        </div>
      </div>
      <div>
        <h3 class="font-bold text-xl mt-6 mb-4">
          Steps
        </h3>
        <ol class="list-decimal list-inside">
          <li v-for="(step, index) in recipe.steps" :key="index" class="pb-3">{{ step }}</li>
        </ol>
      </div>
    </div>
    <form @submit.prevent="generateRecipe" class="fixed bottom-0 w-full max-w-md mx-auto left-0 right-0 bg-zinc-950 border-t border-zinc-200 dark:border-zinc-800 shadow-lg">
       <div class="flex gap-2">
      <input placeholder="Type a dish name" type="text" class="flex-1 dark:bg-zinc-800 p-2 border border-zinc-500 dark:border-zinc-700 rounded shadow-xl text-white" v-model="dishname" />    
      <button class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer" >Generate</button>
      </div>
    </form>
  
</div>
</template>

<script setup lang="ts">
import { ref, type Ref } from 'vue';
interface Ingredients{
  name: string
  quantity: string
}
interface Recipe{
    name: string
    ingredients: Ingredients[]
    steps: string[]
}
    

const recipe: Ref<Recipe> = ref({} as Recipe)
const dishname = ref('')
const loading = ref(false)
const error: Ref<string | null> = ref(null)

const generateRecipe = async() => {
  loading.value = true
  try {
    const response = await fetch('http://localhost:8000/api/ai-chat', {
      method: 'POST',
      headers: {
        "Content-Type": "application/json"
      },
       body: JSON.stringify({dish_name: dishname.value})
    });
    recipe.value = await response.json();
    console.log('jsah', recipe.value)
  } catch (err) {
    console.error('Error fetching recipe:', err);
    error.value = err instanceof Error ? err.message : 'Something went wrong';
  }finally {
    loading.value = false
    dishname.value = ''
  }
}

</script>
<style>
.recipe-wrapper{
  color: white;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.recipe-wrapper::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.recipe-wrapper {
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
</style>
