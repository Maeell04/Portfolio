import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProductDetails from '../views/ProductDetails.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView, // Page d'accueil
    },
    {
      path: '/products',
      name: 'products',
      component: () => import('../views/ProductsView.vue'), // Page produits (si nécessaire)
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue'), // Page contact (si nécessaire)
    },
    {
      path: '/cart',
      name: 'cart',
      component: () => import('../views/CartView.vue'), // Page panier (si nécessaire)
    },
    {
      path: '/product/:id',
      name: 'product',
      component: ProductDetails,
      props: route => ({ id: route.params.id }),
    },
  ],
});

export default router;
