<template>
    <div class="p-4 max-w-3xl mx-auto min-h-screen">
        <h2 class="text-2xl font-bold mb-4 text-primary">Your Cart:</h2>
        <div v-if="cart.items.length === 0">Cart is empty.</div>
        <div v-else>
            <div
                v-for="item in cart.items"
                :key="item.id"
                class="mb-4 border-b pb-2"
            >
                <div class="flex justify-between items-center">
                    <div>
                        <h3 class="text-lg font-semibold">{{ item.title }}</h3>
                        <p>Quantity: {{ item.quantity }}</p>
                        <p>${{ item.price.toFixed(2) }}</p>
                    </div>
                    <button
                        @click="cart.removeFromCart(item.id)"
                        class="text-primary cursor-pointer"
                    >
                        Remove
                    </button>
                </div>
            </div>
            <div class="mt-4 text-xl font-bold">
                Total: ${{ cart.totalPrice.toFixed(2) }}
            </div>
        </div>
    </div>
</template>

<script setup>
    import { useCartStore } from "../stores/useCartStore";
    const cart = useCartStore();
</script>
