<template>
    <div
        class="p-4 max-w-4xl mx-auto"
        v-if="book"
    >
        <h1 class="text-3xl font-bold mb-4">{{ book.title }}</h1>
        <img
            :src="book.cover_url"
            alt="Cover"
            class="w-64 rounded mb-4"
        />
        <p class="text-lg mb-2"><strong>Author:</strong> {{ book.author }}</p>
        <p class="text-md mt-4">{{ book.description }}</p>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import axios from "axios";

    const route = useRoute();
    const book = ref(null);

    onMounted(async () => {
        const res = await axios.get(
            `http://localhost:5002/books/${route.params.id}`
        );
        book.value = res.data;
    });
</script>
