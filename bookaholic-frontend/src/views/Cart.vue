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
                        class="cursor-pointer border-1 border-primary text-sm bg-white font-bold text-primary px-2 py-1 rounded hover:bg-primary hover:text-white"
                    >
                        Remove
                    </button>
                </div>
            </div>

            <div class="mt-4 text-xl font-bold">
                Total: ${{ cart.totalPrice.toFixed(2) }}
            </div>

            <button
                @click="placeOrder"
                class="cursor-pointer mt-6 px-6 py-2 bg-primary text-white rounded hover:bg-opacity-90"
            >
                Buy Now
            </button>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { useCartStore } from "../stores/useCartStore";
    import axios from "axios";

    interface CartItem {
        id: number;
        title: string;
        price: number;
        quantity: number;
        cover_url: string;
    }

    interface OrderItem {
        book_id: number;
        quantity: number;
        price: number;
    }

    interface OrderPayload {
        user_id: number;
        total_amount: number;
        items: OrderItem[];
    }

    const cart = useCartStore();

    async function placeOrder(): Promise<void> {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in to place an order.");
            return;
        }

        try {
            const payload = JSON.parse(atob(token.split(".")[1])) as {
                user_id: number;
            };
            const userId = payload.user_id;

            const orderData: OrderPayload = {
                user_id: userId,
                total_amount: cart.totalPrice,
                items: cart.items.map((item: CartItem) => ({
                    book_id: item.id,
                    quantity: item.quantity,
                    price: item.price,
                })),
            };

            const res = await axios.post(
                "http://localhost:5003/orders",
                orderData,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            alert("Order placed successfully!");
            cart.clearCart();
        } catch (error) {
            console.error("Order failed:", error);
            alert("Failed to place order.");
        }
    }
</script>
