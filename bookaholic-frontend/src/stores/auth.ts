import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        token: null as string | null,
    }),
    getters: {
        isLoggedIn: (state) => !!state.token,
    },
    actions: {
        login(token: string) {
            this.token = token;
            localStorage.setItem("token", token);
        },
        logout() {
            this.token = null;
            localStorage.removeItem("token");
        },
        restore() {
            this.token = localStorage.getItem("token");
        },
    },
});
