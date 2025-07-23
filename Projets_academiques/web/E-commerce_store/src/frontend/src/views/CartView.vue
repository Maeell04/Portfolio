<template>
  <div>
    <header>
      <h1>My E-commerce</h1>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/cart">Cart</router-link>
      </nav>
    </header>

    <div v-if="cart.length > 0">
      <h2>Your Cart</h2>
      <ul>
        <li v-for="item in cart" :key="item.id" class="cart-item">
          <span>
            {{ item.name }} - ${{ item.price.toFixed(2) }} × {{ item.quantity }} = $
            {{ (item.price * item.quantity).toFixed(2) }}
          </span>
          <button @click="removeFromCart(item.id)">Remove 1</button>
        </li>
      </ul>
      <hr />
      <p><strong>Cart Total:</strong> ${{ cartTotal.toFixed(2) }}</p>
      <p><strong>Estimated Delivery Time:</strong> {{ estimatedDeliveryTime }} days</p>
      <div class="promo">
        <label for="promo-code">Promo Code</label>
        <input
          id="promo-code"
          v-model="promoCode"
          placeholder="Enter promo code"
        />
        <button @click="applyPromoCode">Apply</button>
        <p v-if="promoApplied" class="promo-applied">
          Promo code applied! 10% discount added.
        </p>
      </div>
      <hr />
      <h3>Available Payment Methods:</h3>
      <ul>
        <li>💳 Credit Card</li>
        <li>💸 PayPal</li>
        <li>📱 Apple Pay / Google Pay</li>
      </ul>
      <button class="pay-now">Pay Now</button>
    </div>
    <div v-else class="empty-cart">
      <h2>Your Cart is Empty</h2>
      <router-link to="/">Start Shopping</router-link>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      cart: [],
      promoCode: "",
      promoApplied: false,
    };
  },
  computed: {
    cartTotal() {
      const total = this.cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
      return this.promoApplied ? total * 0.9 : total;
    },
    estimatedDeliveryTime() {
      if (this.cart.length === 0) return 0;
      return Math.max(...this.cart.map((item) => item.delivery));
    },
  },
  methods: {
    loadCart() {
      this.cart = JSON.parse(localStorage.getItem("cart")) || [];
    },
    removeFromCart(productId) {
      const itemIndex = this.cart.findIndex((item) => item.id === productId);
      if (itemIndex > -1) {
        if (this.cart[itemIndex].quantity > 1) {
          this.cart[itemIndex].quantity -= 1;
        } else {
          this.cart.splice(itemIndex, 1);
        }
        localStorage.setItem("cart", JSON.stringify(this.cart));
      }
    },
    applyPromoCode() {
      if (this.promoCode.trim().toLowerCase() === "christmas10") {
        this.promoApplied = true;
      } else {
        alert("Invalid promo code");
      }
    },
  },
  mounted() {
    this.loadCart();
  },
};
</script>

<style>
.cart-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.promo {
  margin-top: 20px;
}

.promo-applied {
  color: green;
  margin-top: 10px;
}

.empty-cart {
  text-align: center;
  margin-top: 50px;
}

.pay-now {
  background-color: #333;
  color: #fff;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  margin-top: 20px;
}

.pay-now:hover {
  background-color: #555;
}
</style>
