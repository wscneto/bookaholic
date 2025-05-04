<template>
    <div
        class="flex flex-col items-center justify-center min-h-screen bg-white text-gray-800"
    >
        <h2 class="text-3xl font-bold mb-6 text-primary">
            {{ isLogin ? "Login to Bookaholic" : "Create your account" }}
        </h2>

        <form
            @submit.prevent="handleSubmit"
            class="w-full max-w-sm bg-gray-50 p-6 rounded-xl shadow"
        >
            <div
                v-if="!isLogin"
                class="mb-4"
            >
                <label class="block mb-1 font-semibold">Name</label>
                <input
                    v-model="form.name"
                    type="text"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
                    required
                />
            </div>

            <div class="mb-4">
                <label class="block mb-1 font-semibold">Email</label>
                <input
                    v-model="form.email"
                    type="email"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
                    required
                />
            </div>

            <div class="mb-6">
                <label class="block mb-1 font-semibold">Password</label>
                <input
                    v-model="form.password"
                    type="password"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
                    required
                />
            </div>

            <button
                type="submit"
                class="w-full bg-primary text-white py-2 rounded-xl font-bold hover:opacity-90 transition cursor-pointer"
            >
                {{ isLogin ? "Login" : "Register" }}
            </button>

            <p class="mt-4 text-sm text-center">
                {{
                    isLogin
                        ? "Don't have an account?"
                        : "Already have an account?"
                }}
                <RouterLink
                    :to="{
                        name: 'auth',
                        query: { login: (!isLogin).toString() },
                    }"
                    class="text-primary font-semibold underline ml-1 cursor-pointer"
                >
                    {{ isLogin ? "Register" : "Login" }}
                </RouterLink>
            </p>
        </form>
    </div>
</template>

<script lang="ts" setup>
    import { reactive, computed, watch } from "vue";
    import { useRoute, useRouter } from "vue-router";
    import axios from "axios";

    const route = useRoute();
    const router = useRouter();

    const isLogin = computed(() => route.query.login === "true");

    const form = reactive({
        name: "",
        email: "",
        password: "",
    });

    const handleSubmit = async () => {
        try {
            if (isLogin.value) {
                const res = await axios.post("http://localhost:5001/login", {
                    email: form.email,
                    password: form.password,
                });
                localStorage.setItem("token", res.data.token);
                alert("Login successful!");
                // redirect to homepage or dashboard
                router.push("/");
            } else {
                const password_hash = form.password; // let backend hash it
                await axios.post("http://localhost:5001/users", {
                    name: form.name,
                    email: form.email,
                    password_hash,
                });
                alert("Registration successful! You can now login.");
                router.push({ name: "auth", query: { login: "true" } });
            }
        } catch (err: any) {
            alert("Error: " + (err.response?.data?.error || err.message));
        }
    };
</script>

<style scoped></style>
