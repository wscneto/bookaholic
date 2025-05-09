<template>
    <div class="p-6 max-w-6xl mx-auto min-h-screen">
        <h2 class="text-2xl font-bold mb-4 text-primary">
            Recommended for You:
        </h2>

        <div v-if="isLoading">Loading recommendations...</div>
        <div v-else-if="books.length === 0">
            No recommendations yet. Try adding books to your wishlist!
        </div>

        <div
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
            <BookCard
                v-for="book in books"
                :key="book.id"
                :book="book"
            />
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, onMounted } from "vue";
    import axios from "axios";
    import BookCard from "../components/BookCard.vue";

    interface Book {
        id: number;
        title: string;
        author: string;
        description: string;
        price: number;
        cover_url: string;
    }

    const books = ref<Book[]>([]);
    const isLoading = ref(true);

    onMounted(async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in to see recommendations.");
            return;
        }

        try {
            const res = await axios.get(
                "http://localhost:5005/recommendations",
                {
                    headers: { Authorization: `Bearer ${token}` },
                }
            );
            books.value = res.data;
        } catch (error) {
            console.error("Error fetching recommendations:", error);
            alert("Could not load recommendations.");
        } finally {
            isLoading.value = false;
        }
    });
</script>
