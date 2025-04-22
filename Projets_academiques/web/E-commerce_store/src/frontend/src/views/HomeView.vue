<template>
  <div>
    <!-- Header commun -->
    <header>
      <h1>My E-commerce</h1>
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/contact">Contact</a></li>
          <li><a href="/cart">Cart</a></li>
        </ul>
      </nav>
    </header>

    <!-- Product Section -->
    <section class="products">
      <div class="product-item">
        <img src="@/assets/Product1.jpg" alt="Moon Lamp" />
        <p class="price">$29.99</p>
        <button class="buy-now" @click="goToProduct(1)">Buy Now</button>
      </div>
      <div class="product-item">
        <img src="@/assets/Product2.jpg" alt="Crystal Heart Lamp" />
        <p class="price">$39.99</p>
        <button class="buy-now" @click="goToProduct(2)">Buy Now</button>
      </div>
      <div class="product-item">
        <img src="@/assets/Product3.jpg" alt="Duck Night Light" />
        <p class="price">$19.99</p>
        <button class="buy-now" @click="goToProduct(3)">Buy Now</button>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: "HomeView",
  methods: {
    goToProduct(id) {
      this.$router.push(`/product/${id}`);
    },
  },
};
</script>

<style>
/* Styles pour le header */
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #333;
  padding: 1rem 2rem;
  color: white;
}

header h1 {
  font-size: 1.5rem;
}

header nav ul {
  list-style: none;
  display: flex;
  gap: 1rem;
}

header nav ul li a {
  text-decoration: none;
  color: white;
  font-weight: bold;
}

header nav ul li a:hover {
  text-decoration: underline;
}

/* Styles pour les produits */
.products {
  display: flex;
  justify-content: space-around;
  margin: 2rem 0;
}

.product-item {
  text-align: center;
}

.product-item img {
  width: 250px;
  height: auto;
  border-radius: 10px;
}

.price {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 0.5rem 0;
}

.buy-now {
  background-color: #333; /* Noir */
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.buy-now:hover {
  background-color: #555; /* Gris clair */
}
</style>
