<template>
    <div
        class="min-h-screen mt-10 flex flex-row justify-center gap-10"
        v-if="book"
    >
        <div class="p-4 max-w-4xl">
            <img
                :src="book.cover_url"
                alt="Cover"
                class="w-64 rounded mb-4"
            />
            <p class="text-lg mb-2">
                <strong>Remaining quantity:</strong> {{ book.stock }}
            </p>
            <p class="text-lg mb-2">
                <strong>Author:</strong> {{ book.author }}
            </p>
            <p class="max-w-sm text-md mt-4">{{ book.description }}</p>
        </div>

        <div class="mt-5">
            <h1 class="max-w-sm text-3xl font-bold mb-4">{{ book.title }}</h1>
            <div
                @click="handleAddToCart"
                class="pi pi-cart-plus cursor-pointer bg-white border-2 border-primary p-3 rounded-full text-primary hover:text-white hover:bg-primary transition"
                style="font-size: 1.5rem"
            ></div>
        </div>
    </div>
</template>

<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";
    import axios from "axios";
    import { useCartStore } from "../stores/useCartStore";

    const route = useRoute();
    const book = ref(null);
    const cart = useCartStore();
    const token = localStorage.getItem("token");

    function handleAddToCart() {
        if (!token) {
            alert("Please log in first.");
            return;
        }
        cart.addToCart({
            id: book.value.id,
            title: book.value.title,
            price: book.value.price,
            cover_url: book.value.cover_url,
        });
    }

    onMounted(async () => {
        const res = await axios.get(
            `http://localhost:5002/books/${route.params.id}`
        );
        book.value = res.data;
    });
</script>
