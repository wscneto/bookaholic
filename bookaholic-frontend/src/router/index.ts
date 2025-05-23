import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import AuthPage from "../views/AuthPage.vue";
import SearchResults from "../views/SearchResults.vue";
import BookDetails from "../views/BookDetails.vue";
import Cart from "@/views/Cart.vue";
import Wishlist from "@/views/Wishlist.vue";
import Orders from "@/views/Orders.vue";
import Recommendations from "@/views/Recommendations.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: "/",
            name: "home",
            component: Home,
        },
        {
            path: "/auth",
            name: "auth",
            component: AuthPage,
        },
        {
            path: "/search",
            name: "search",
            component: SearchResults,
        },
        {
            path: "/books/:id",
            name: "bookdetails",
            component: BookDetails,
        },
        {
            path: "/cart",
            name: "cart",
            component: Cart,
        },
        {
            path: "/wishlist",
            name: "wishlist",
            component: Wishlist,
        },
        {
            path: "/orders",
            name: "orders",
            component: Orders,
        },
        {
            path: "/recommendations",
            name: "recommendations",
            component: Recommendations,
        },
    ],
});

export default router;
