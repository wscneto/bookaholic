<template>
    <div class="p-4 min-h-screen">
        <h1 class="text-2xl mb-4 font-bold text-primary">Search Results:</h1>
        <div v-if="loading">Loading...</div>
        <div v-else-if="results.length === 0">No books found.</div>
        <div
            v-else
            class="grid grid-cols-2 md:grid-cols-4 gap-4"
        >
            <BookCard
                v-for="book in results"
                :key="book.id"
                :book="book"
            />
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, onMounted, watch } from "vue";
    import { useRoute } from "vue-router";
    import axios from "axios";
    import BookCard from "../components/BookCard.vue";

    const route = useRoute();
    const results = ref<any[]>([]);
    const loading = ref(true);

    const fetchResults = async () => {
        loading.value = true;
        const q = route.query.q as string;
        if (q) {
            const res = await axios.get(
                `http://localhost:5002/books/search?q=${encodeURIComponent(q)}`
            );
            results.value = res.data;
        } else {
            results.value = [];
        }
        loading.value = false;
    };

    onMounted(fetchResults);
    watch(() => route.query.q, fetchResults);
</script>
