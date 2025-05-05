<template>
    <div
        class="flex flex-col items-center justify-center min-h-screen bg-white text-gray-800"
    >
        <h1 class="text-4xl font-bold text-primary mb-8">
            Welcome to Bookaholic
        </h1>
    </div>

    <h2 class="text-3xl font-bold text-primary mb-8 text-center">
        See our collection:
    </h2>
    <BooksCarousel />
</template>

<script lang="ts" setup>
    import BooksCarousel from "../components/BooksCarousel.vue";
</script>
