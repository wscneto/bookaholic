import { defineStore } from "pinia";
import { useCartStore } from "./useCartStore";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        token: null as string | null,
    }),
    getters: {
        isLoggedIn: (state) => !!state.token,
    },
    actions: {
        login(token: string) {
            useCartStore().clearCart();
            this.token = token;
            localStorage.setItem("token", token);
        },
        logout() {
            useCartStore().clearCart();
            this.token = null;
            localStorage.removeItem("token");
        },
        restore() {
            this.token = localStorage.getItem("token");
        },
    },
});
