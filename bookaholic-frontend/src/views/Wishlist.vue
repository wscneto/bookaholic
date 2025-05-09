<template>
    <div class="p-4 max-w-5xl mx-auto min-h-screen">
        <h2 class="text-2xl font-bold mb-4 text-primary">Your Wishlist:</h2>
        <div v-if="books.length === 0">Your wishlist is empty.</div>
        <div
            v-else
            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6"
        >
            <div
                v-for="book in books"
                :key="book.id"
                class="relative"
            >
                <BookCard :book="book" />
                <button
                    @click="removeFromWishlist(book.id)"
                    class="cursor-pointer border-1 border-primary absolute bottom-3 right-18 text-sm bg-white font-bold text-primary px-2 py-1 rounded hover:bg-primary hover:text-white"
                >
                    Remove
                </button>
            </div>
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
        cover_url: string;
        price: number;
        stock: number;
    }

    const books = ref<Book[]>([]);

    onMounted(async () => {
        try {
            const token = localStorage.getItem("token");
            const wishlistRes = await axios.get<Book[]>(
                "http://localhost:5001/wishlist",
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            books.value = wishlistRes.data;
        } catch (error) {
            console.error("Failed to load wishlist:", error);
        }
    });

    async function removeFromWishlist(bookId: number) {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in first.");
            return;
        }

        try {
            await axios.delete(`http://localhost:5001/wishlist/${bookId}`, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            books.value = books.value.filter((b) => b.id !== bookId);
            alert("Removed from wishlist!");
        } catch (error) {
            console.error("Failed to remove from wishlist:", error);
            alert("Failed to remove from wishlist.");
        }
    }
</script>
