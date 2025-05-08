<template>
    <nav
        class="sticky top-0 z-50 bg-white border-b border-gray-200 px-4 py-3 flex justify-between items-center shadow-sm"
    >
        <router-link
            to="/"
            class="text-xl font-bold text-primary"
            >Bookaholic</router-link
        >

        <div class="flex items-center gap-4">
            <form
                @submit.prevent="onSearch"
                class="flex items-center"
            >
                <input
                    v-model="searchTerm"
                    type="text"
                    placeholder="Search books"
                    class="px-5 py-2 rounded-l border"
                />
                <button
                    type="submit"
                    class="cursor-pointer bg-primary border-1 border-primary text-white px-5 py-2 rounded-r hover:opacity-90 font-semibold"
                >
                    <span class="pi pi-search"></span>
                </button>
            </form>
            <div
                v-if="!auth.isLoggedIn"
                class="flex items-center gap-4"
            >
                <router-link
                    to="/auth?login=true"
                    class="bg-white border-1 border-primary text-primary px-6 py-3 rounded-xl font-semibold hover:opacity-90 hover:bg-primary hover:text-white transition"
                    >Login</router-link
                >
                <router-link
                    to="/auth?login=false"
                    class="bg-white border-1 border-primary text-primary px-6 py-3 rounded-xl font-semibold hover:opacity-90 hover:bg-primary hover:text-white transition"
                    >Register</router-link
                >
            </div>
            <div
                v-else
                class="flex items-center gap-4"
            >
                <router-link
                    to="/cart"
                    class="pi pi-shopping-cart cursor-pointer bg-white border-1 border-primary text-primary p-4 rounded-full hover:bg-primary hover:text-white transition"
                ></router-link>
                <router-link to="/">
                    <button
                        @click="auth.logout()"
                        class="cursor-pointer bg-white border-1 border-primary text-primary px-6 py-3 rounded-xl font-semibold hover:opacity-90 hover:bg-primary hover:text-white transition"
                    >
                        Logout
                    </button>
                </router-link>
            </div>
        </div>
    </nav>
</template>

<script lang="ts" setup>
    import { ref } from "vue";
    import { useRouter } from "vue-router";
    import { useAuthStore } from "@/stores/auth";

    const auth = useAuthStore();
    const searchTerm = ref("");
    const router = useRouter();
    auth.restore();

    const onSearch = () => {
        if (searchTerm.value.trim()) {
            router.push({ name: "search", query: { q: searchTerm.value } });
        }
    };
</script>
