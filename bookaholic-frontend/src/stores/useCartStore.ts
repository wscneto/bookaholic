import { defineStore } from "pinia";

function isUserLoggedIn() {
    return !!localStorage.getItem("token");
}

export const useCartStore = defineStore("cart", {
    state: () => ({
        items: [] as {
            id: number;
            title: string;
            price: number;
            cover_url: string;
            quantity: number;
        }[],
    }),
    getters: {
        totalPrice: (state) =>
            state.items.reduce(
                (total, item) => total + item.price * item.quantity,
                0
            ),
        itemCount: (state) =>
            state.items.reduce((sum, item) => sum + item.quantity, 0),
    },
    actions: {
        addToCart(book: {
            id: number;
            title: string;
            price: number;
            cover_url: string;
        }) {
            if (!isUserLoggedIn()) {
                alert("Please log in to add items to your cart.");
                return;
            }
            const existing = this.items.find((item) => item.id === book.id);
            if (existing) {
                existing.quantity += 1;
            } else {
                this.items.push({
                    ...book,
                    quantity: 1,
                    price: Number(book.price),
                });
            }
        },
        removeFromCart(id: number) {
            this.items = this.items.filter((item) => item.id !== id);
        },
        clearCart() {
            this.items = [];
        },
    },
    persist: true,
});
