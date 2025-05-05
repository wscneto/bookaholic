<template>
    <router-link :to="`/books/${book.id}`">
        <div class="p-4 bg-white rounded-lg shadow-md w-64">
            <img
                :src="book.cover_url"
                alt="Book Cover"
                class="w-full h-64 object-cover rounded-md mb-3"
            />
            <h3 class="text-lg font-bold mb-1">{{ book.title }}</h3>
            <p class="text-sm text-gray-700">
                {{ truncatedDescription }}
            </p>
            <p class="text-sm font-bold text-gray-700 mt-3">
                ${{ book.price }}
            </p>
        </div>
    </router-link>
</template>

<script lang="ts" setup>
    import { computed } from "vue";
    const props = defineProps<{
        book: {
            id: number;
            title: string;
            description: string;
            price: number;
            cover_url: string;
        };
    }>();

    const charLimit = 100;

    const truncatedDescription = computed(() => {
        return props.book.description.length > charLimit
            ? props.book.description.slice(0, charLimit) + "..."
            : props.book.description;
    });
</script>

<style scoped>
    div:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
    }
</style>
