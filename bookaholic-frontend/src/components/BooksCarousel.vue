<template>
    <Carousel
        :value="books"
        :numVisible="4"
        :numScroll="1"
        :responsiveOptions="responsiveOptions"
        circular
        :autoplayInterval="2500"
    >
        <template #item="slotProps">
            <router-link :to="`/books/${slotProps.data.id}`">
                <div class="p-4 bg-white rounded-lg shadow-md w-64">
                    <img
                        :src="slotProps.data.cover_url"
                        alt="Book Cover"
                        class="w-full h-64 object-cover rounded-md mb-3"
                    />
                    <h3 class="text-lg font-bold mb-1">
                        {{ slotProps.data.title }}
                    </h3>
                    <p class="text-sm text-gray-700">
                        {{
                            slotProps.data.description.length > 100
                                ? slotProps.data.description.slice(0, 100) +
                                  "..."
                                : slotProps.data.description
                        }}
                    </p>
                    <p class="text-sm font-bold text-gray-700 mt-3">
                        ${{ slotProps.data.price }}
                    </p>
                </div>
            </router-link>
        </template>
    </Carousel>
</template>

<script lang="ts" setup>
    import { ref, onMounted } from "vue";
    import axios from "axios";

    const books = ref([]);
    const responsiveOptions = ref([
        {
            breakpoint: "1400px",
            numVisible: 4,
            numScroll: 1,
        },
        {
            breakpoint: "1199px",
            numVisible: 3,
            numScroll: 1,
        },
        {
            breakpoint: "767px",
            numVisible: 2,
            numScroll: 1,
        },
        {
            breakpoint: "575px",
            numVisible: 1,
            numScroll: 1,
        },
    ]);

    onMounted(async () => {
        try {
            const res = await axios.get("http://localhost:5002/books");
            books.value = res.data;
        } catch (error) {
            console.error("Failed to load books:", error);
        }
    });
</script>
