<template>
    <div class="min-h-screen bg-white text-gray-900">
        <NavBar />
        <router-view />
        <Footer />
    </div>
</template>

<script lang="ts" setup>
    import NavBar from "./components/NavBar.vue";
    import Footer from "./components/Footer.vue";
</script>
