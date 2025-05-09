<template>
    <div class="p-6 max-w-4xl mx-auto min-h-screen">
        <h2 class="text-2xl font-bold mb-6 text-primary">Your Orders:</h2>

        <div v-if="orders.length === 0">You have no orders.</div>

        <div
            v-for="order in orders"
            :key="order.id"
            class="mb-6 border-b pb-6"
        >
            <h3 class="text-lg font-semibold mb-2">
                Order #{{ order.id }} — ${{
                    Number(order.total_amount).toFixed(2)
                }}
            </h3>
            <p class="text-sm text-gray-600 mb-4">Status: {{ order.status }}</p>

            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                <div
                    v-for="item in order.items"
                    :key="item.book_id"
                    class="flex flex-col items-center bg-white p-3 rounded shadow"
                >
                    <img
                        :src="item.cover_url"
                        alt="Book Cover"
                        class="w-32 h-48 object-cover rounded mb-2"
                    />
                    <h4 class="text-sm font-bold text-center mb-1">
                        {{ item.title }}
                    </h4>
                    <p class="text-xs text-gray-700 text-center">
                        Quantity: {{ item.quantity }}<br />
                        Price: ${{ Number(item.price).toFixed(2) }}
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts" setup>
    import { ref, onMounted } from "vue";
    import axios from "axios";

    interface OrderItem {
        book_id: number;
        title: string;
        quantity: number;
        price: number | string;
        cover_url: string;
    }

    interface Order {
        id: number;
        total_amount: number | string;
        status: string;
        items: OrderItem[];
    }

    const orders = ref<Order[]>([]);

    onMounted(async () => {
        const token = localStorage.getItem("token");
        if (!token) {
            alert("Please log in.");
            return;
        }

        try {
            const payload = JSON.parse(atob(token.split(".")[1]));
            const userId = payload.user_id;

            const res = await axios.get<Order[]>(
                `http://localhost:5003/orders/user/${userId}`,
                {
                    headers: {
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            // Safely parse number fields
            orders.value = res.data.map((order) => ({
                ...order,
                total_amount: Number(order.total_amount),
                items: order.items.map((item) => ({
                    ...item,
                    price: Number(item.price),
                })),
            }));
        } catch (error) {
            console.error("Error fetching orders:", error);
            alert("Could not load orders.");
        }
    });
</script>
