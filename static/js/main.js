// Sample categories
const categories = ["All", "Electronics", "Clothing", "Books", "Accessories"];

// Sample product data
const products = [
    { id: 1, name: "Smartphone", category: "Electronics", price: 399.99, image: "/static/images/smartphone.jpg" },
    { id: 2, name: "T-Shirt", category: "Clothing", price: 19.99, image: "/static/images/tshirt.jpg" },
    { id: 3, name: "Laptop", category: "Electronics", price: 799.99, image: "/static/images/laptop.jpg" },
    { id: 4, name: "Novel", category: "Books", price: 14.99, image: "/static/images/book.jpg" }
];

// Cart
let cart = [];

// Function to render categories
function renderCategories() {
    const categoryList = document.getElementById("category-list");
    categoryList.innerHTML = categories.map(category =>
        `<li onclick="filterProducts('${category}')">${category}</li>`
    ).join("");
}

// Function to render products
function renderProducts(filteredCategory = "All") {
    const productList = document.getElementById("product-list");
    productList.innerHTML = products
        .filter(product => filteredCategory === "All" || product.category === filteredCategory)
        .map(product => `
            <div class="product" data-id="${product.id}">
              <img src="${product.image}" alt="${product.name}">
              <h3>${product.name}</h3>
              <p>$${product.price.toFixed(2)}</p>
              <button onclick="addToCart(${product.id})">Add to Cart</button>
            </div>
        `).join("");
}

// Function to filter products by category
function filterProducts(category) {
    renderProducts(category);
}

// Function to add a product to the cart
function addToCart(productId) {
    const product = products.find(p => p.id === productId);
    if (product) {
        cart.push(product);
        alert(`${product.name} added to cart!`);
    }
}

// Initial render
document.addEventListener("DOMContentLoaded", () => {
    renderCategories();
    renderProducts();
});


// Function to add a product to the cart
function addToCart(productId) {
  fetch("/add_to_cart", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ product_id: productId }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          alert(data.message);
      } else {
          alert("Error adding to cart.");
      }
  })
  .catch(error => console.error("Error:", error));
}

function removeFromCart(cartItemId) {
  fetch("/remove_from_cart", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify({ cart_item_id: cartItemId }),
  })
  .then(response => response.json())
  .then(data => {
      if (data.message) {
          alert(data.message);
          location.reload(); // Refresh page to update cart
      } else {
          alert("Error removing item.");
      }
  })
  .catch(error => console.error("Error:", error));
}
