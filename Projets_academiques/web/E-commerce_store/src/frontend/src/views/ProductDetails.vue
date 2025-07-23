<template>
  <div v-if="product">
    <h1 style="font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 20px;">
      {{ product.name }}
    </h1>
    <div style="text-align: center; margin-bottom: 20px;">
      <img :src="product.image" :alt="product.name" style="width: 60%; height: auto; border-radius: 10px;" />
    </div>
    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 20px;">
      {{ product.description }}
    </p>
    <table style="margin: 0 auto; border-collapse: collapse; width: 80%; margin-bottom: 20px;">
      <thead>
        <tr style="background-color: #f4f4f4;">
          <th style="text-align: left; padding: 10px; border: 1px solid #ddd;">Attribute</th>
          <th style="text-align: left; padding: 10px; border: 1px solid #ddd;">Details</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(value, key) in product.details" :key="key">
          <td style="padding: 10px; border: 1px solid #ddd;">{{ key }}</td>
          <td style="padding: 10px; border: 1px solid #ddd;">{{ value }}</td>
        </tr>
      </tbody>
    </table>
    <div style="text-align: center; font-size: 1.1rem; margin-bottom: 20px;">
      <p><strong>Price:</strong> ${{ product.price }}</p>
      <p><strong>Stock:</strong> {{ product.stock }} items available</p>
      <p><strong>Delivery Time:</strong> {{ product.delivery }} days</p>
    </div>
    <div style="text-align: center;">
      <button
        @click="addToCart"
        style="background-color: #333; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;"
      >
        Add to Cart
      </button>
    </div>
  </div>
  <div v-else>
    <p style="text-align: center;">Loading product details...</p>
  </div>
</template>

<script>
import Product1Image from "@/assets/Product1.jpg";
import Product2Image from "@/assets/Product2.jpg";
import Product3Image from "@/assets/Product3.jpg";

export default {
  name: "ProductDetails",
  props: {
    id: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      product: null,
    };
  },
  methods: {
    addToCart() {
      const cart = JSON.parse(localStorage.getItem("cart")) || [];
      const existingProduct = cart.find((item) => item.id === this.product.id);
      if (existingProduct) {
        existingProduct.quantity += 1;
      } else {
        cart.push({ ...this.product, quantity: 1 });
      }
      localStorage.setItem("cart", JSON.stringify(cart));
      alert(`${this.product.name} has been added to your cart!`);
    },
  },
  mounted() {
    const products = {
      1: {
        name: "Moon Lamp",
        image: Product1Image,
        price: 29.99,
        stock: Math.floor(Math.random() * 20) + 1,
        delivery: Math.floor(Math.random() * 7) + 2,
        description: "This Moon Lamp brings the beauty of the moon into your home, perfect for a cozy night or as a unique decorative piece.",
        details: {
          Weight: "500g",
          Size: "15cm diameter",
          Material: "PLA (Eco-Friendly)",
          Energy: "Rechargeable Battery",
        },
      },
      2: {
        name: "Crystal Heart Lamp",
        image: Product2Image,
        price: 39.99,
        stock: Math.floor(Math.random() * 15) + 1,
        delivery: Math.floor(Math.random() * 5) + 3,
        description: "A stunning Crystal Heart Lamp that radiates love and warmth, perfect as a gift or for a romantic setting.",
        details: {
          Weight: "1.2kg",
          Size: "10cm x 10cm",
          Material: "Crystal Glass",
          Energy: "Plug-in Power",
        },
      },
      3: {
        name: "Duck Night Light",
        image: Product3Image,
        price: 19.99,
        stock: Math.floor(Math.random() * 30) + 5,
        delivery: Math.floor(Math.random() * 3) + 1,
        description: "Adorable Duck Night Light perfect for children or anyone who loves a cute addition to their nightstand.",
        details: {
          Weight: "300g",
          Size: "12cm x 10cm x 10cm",
          Material: "Silicone",
          Energy: "Battery-Powered",
        },
      },
    };

    const productId = this.id;
    this.product = products[productId] || null;

    if (!this.product) {
      console.error("Product not found!");
    }
  },
};
</script>

<style>
/* Styles global */
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

.product-details {
  margin: 2rem auto;
}

.product-details img {
  max-width: 300px;
  margin: 1rem 0;
}

table {
  margin: 1rem auto;
  border-collapse: collapse;
  width: 50%;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 8px;
}

table th {
  background-color: #f4f4f4;
}

.add-to-cart {
  background-color: #333;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.add-to-cart:hover {
  background-color: #555;
}
</style>
