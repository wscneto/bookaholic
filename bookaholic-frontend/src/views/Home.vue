<template>
    <div
        class="flex flex-col items-center justify-center min-h-screen bg-white text-gray-800"
    >
        <h1 class="text-4xl font-bold text-primary mb-8">
            Welcome to Bookaholic
        </h1>

        <div class="flex gap-6">
            <router-link
                :to="{ name: 'auth', query: { login: 'true' } }"
                class="bg-white border-2 border-primary text-primary px-6 py-3 rounded-xl text-lg font-semibold hover:opacity-90 hover:bg-primary hover:text-white transition"
            >
                Login
            </router-link>

            <router-link
                :to="{ name: 'auth', query: { login: 'false' } }"
                class="bg-white border-2 border-primary text-primary px-6 py-3 rounded-xl text-lg font-semibold hover:opacity-90 hover:bg-primary hover:text-white transition"
            >
                Register
            </router-link>
        </div>
    </div>
</template>

<script lang="ts" setup></script>

<style scoped></style>
