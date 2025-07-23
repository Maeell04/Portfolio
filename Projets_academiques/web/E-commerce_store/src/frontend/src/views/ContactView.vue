<template>
  <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
    <h1 style="font-size: 2.5rem; font-weight: bold; text-align: center; margin-bottom: 20px;">
      Contact Us
    </h1>
    <p style="text-align: center; font-size: 1.2rem; margin-bottom: 30px;">
      At My E-commerce, we are happy to assist you! Please fill out the form below to get in touch with us.
    </p>
    <form style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);">
      <div style="margin-bottom: 15px;">
        <label for="email" style="display: block; font-weight: bold; margin-bottom: 5px;">Email Address</label>
        <input
          type="email"
          id="email"
          placeholder="Enter your email"
          style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"
          required
        />
      </div>
      <div style="margin-bottom: 15px;">
        <label for="message" style="display: block; font-weight: bold; margin-bottom: 5px;">Message</label>
        <textarea
          id="message"
          rows="5"
          placeholder="Write your message here..."
          style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;"
          required
        ></textarea>
      </div>
      <div style="text-align: center;">
        <button
          type="submit"
          style="background-color: #333; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer;"
        >
          Send Message
        </button>
      </div>
    </form>
  </div>
</template>
