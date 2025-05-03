<template>
    <div class="p-6 max-w-4xl mx-auto">
        <h1 class="text-3xl font-bold mb-6">Online Bookstore</h1>

        <!-- Book List Section -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div
                v-for="book in books"
                :key="book.id"
                class="border p-4 rounded"
            >
                <h2 class="text-xl font-semibold">{{ book.title }}</h2>
                <p>{{ book.author }}</p>
                <p>${{ book.price }}</p>
                <button
                    @click="addToCart(book)"
                    class="mt-2 bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Add to Cart
                </button>
            </div>
        </div>

        <!-- Cart Section -->
        <div
            v-if="cart.length > 0"
            class="mt-8"
        >
            <h2 class="text-2xl font-semibold mb-2">Your Cart</h2>
            <div
                v-for="item in cart"
                :key="item.id"
            >
                <p>{{ item.title }} x {{ item.quantity }}</p>
            </div>
            <div class="mt-4">
                <input
                    v-model="name"
                    placeholder="Your Name"
                    class="border px-2 py-1 w-full mb-2"
                />
                <input
                    v-model="email"
                    placeholder="Your Email"
                    class="border px-2 py-1 w-full mb-4"
                />
                <button
                    @click="placeOrder"
                    :disabled="!cart.length"
                    class="bg-green-500 text-white px-4 py-2 rounded"
                >
                    Place Order
                </button>
            </div>
        </div>

        <!-- Empty Cart Message -->
        <div
            v-else
            class="mt-8"
        >
            <p>Your cart is empty. Add some books!</p>
        </div>
    </div>
</template>

<script lang="ts">
    import { defineComponent, ref, onMounted } from "vue";

    interface Book {
        id: number;
        title: string;
        author: string;
        price: number;
    }

    interface CartItem extends Book {
        quantity: number;
    }

    export default defineComponent({
        name: "BookList",
        setup() {
            const books = ref<Book[]>([]);
            const cart = ref<CartItem[]>([]);
            const name = ref("");
            const email = ref("");

            onMounted(() => {
                fetch("http://localhost:5000/catalog/books")
                    .then((res) => res.json())
                    .then((data) => {
                        books.value = data;
                    });
            });

            const addToCart = (book: Book) => {
                const existingItem = cart.value.find(
                    (item) => item.id === book.id
                );
                if (existingItem) {
                    existingItem.quantity++;
                } else {
                    cart.value.push({ ...book, quantity: 1 });
                }
            };

            const placeOrder = () => {
                fetch("http://localhost:5000/user/users", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        name: name.value,
                        email: email.value,
                        password_hash: "temp123",
                    }),
                })
                    .then((res) => res.json())
                    .then((user) => {
                        const total = cart.value.reduce(
                            (acc, item) => acc + item.price * item.quantity,
                            0
                        );
                        fetch("http://localhost:5000/order/orders", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({
                                user_id: user.id || 1,
                                total_amount: total,
                                items: cart.value.map((item) => ({
                                    book_id: item.id,
                                    price: item.price,
                                    quantity: item.quantity,
                                })),
                            }),
                        })
                            .then((res) => res.json())
                            .then(() => {
                                alert("Order placed!");
                                cart.value = []; // Clear the cart
                            });
                    });
            };

            return {
                books,
                cart,
                name,
                email,
                addToCart,
                placeOrder,
            };
        },
    });
</script>

<style scoped>
    input {
        display: block;
        margin-bottom: 10px;
    }
</style>
