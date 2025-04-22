# E-commerce Store

This project is a full-stack e-commerce web application built using **Vue.js 3 (with Vite)** for the front-end and **Node.js (Express)** for the back-end. It simulates a basic online store with product browsing, cart management, a contact form, and responsive design.

## Project Structure

- `src/` : Vue.js front-end (main application)
- `src/backend/` : Node.js server and basic database configuration
- `captures/` : UI screenshots
- `docs/` : project presentation

## Project Setup

### Install dependencies

```bash
npm install
```

### Compile and Hot-Reload for Development

```bash
npm run dev
```

### Build for Production

```bash
npm run build
```

### Run Unit Tests (Vitest)

```bash
npm run test:unit
```

## Launching the Backend

In the `/src/backend/` folder:

```bash
npm install
node server.js
```

Make sure your backend runs on a different port (e.g. `localhost:3000`) and is correctly linked to the front-end if needed.

## Features

- Responsive design
- Product catalog with details
- Dynamic shopping cart
- Promo code support (in progress)
- Contact form
- Modular front-end structure

## Technologies Used

- Vue.js 3
- Vite
- Node.js + Express
- JavaScript / CSS
