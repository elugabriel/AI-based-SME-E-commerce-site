// Product categories
const categories = ["All", "Phones", "Electronics", "Phones Accessories", "Clothing", "Shoes"];

// Product data
const products = [
  { id: 27, name: "Ipad", category: "Phones", price: 110.00, image: "/static/assets/ipad1.jpg" },
  { id: 15, name: "Unisex shirt", category: "Clothing", price: 89.99, image: "/static/assets/fcloth4.jpg" },
  { id: 42, name: "white canvas", category: "Shoes", price: 30.00, image: "/static/assets/mshoe5.jpg" },
  { id: 6, name: "Earbud", category: "Phones Accessories", price: 15.75, image: "/static/assets/bud.jpg" },
  { id: 33, name: "plain t-shirt", category: "Clothing", price: 140.50, image: "/static/assets/m1.jpg" },
  { id: 48, name: "Android ", category: "Phones", price: 156.99, image: "/static/assets/phone.png" },
  { id: 21, name: "Female Casual Shoe", category: "Shoes", price: 180.20, image: "/static/assets/fshoe5.jpg" },
  { id: 10, name: "charger", category: "Phones Accessories", price: 5.60, image: "/static/assets/charger.jpg" },
  { id: 54, name: "Android", category: "Phones", price: 145.00, image: "/static/assets/phone7.jpg" },
  { id: 3, name: "Arduino Board", category: "Electronics", price: 12.50, image: "/static/assets/board2.jpg" },
  { id: 19, name: "Female Shoe", category: "Shoes", price: 12.50, image: "/static/assets/fshoe3.jpg" },
  { id: 58, name: "selfie stick", category: "Phone Accessories", price: 190.00, image: "/static/assets/stand3.jpg" },
  { id: 36, name: "t-shirt", category: "Clothing", price: 10.00, image: "/static/assets/mcloth3.jpg" },
  { id: 47, name: "Ipad", category: "Phones", price: 600.00, image: "/static/assets/pad4.jpg" },
  { id: 22, name: "casual Shoe", category: "Shoes", price: 2.99, image: "/static/assets/fshoe6.jpg" },
  { id: 5, name: "Sensor", category: "Electronics", price: 22.40, image: "/static/assets/board4.jpg" },
  { id: 14, name: "Gown", category: "Clothing", price: 3.25, image: "/static/assets/fcloth3.jpg" },
  { id: 56, name: "phone stand", category: "Phone Accessories", price: 80.00, image: "/static/assets/stand1.jpg" },
  { id: 25, name: "D-bass", category: "Phone Accessories", price: 75.00, image: "/static/assets/headset.png" },
  { id: 39, name: "Sneaker", category: "Shoes", price: 88.88, image: "/static/assets/mshoe1.jpg" },
  { id: 46, name: "Ipad", category: "phones", price: 350.00, image: "/static/assets/pad3.jpg" },
  { id: 29, name: "Iphone", category: "Phones", price: 160.25, image: "/static/assets/iphone2.jpg" },
  { id: 7, name: "Earbud", category: "Phones Accessories", price: 33.33, image: "/static/assets/bud2.jpg" },
  { id: 43, name: "canvas", category: "Shoes", price: 77.77, image: "/static/assets/mshoe7.jpg" },
  { id: 17, name: "shoe", category: "Shoes", price: 22.40, image: "/static/assets/fshoe1.jpg" },
  { id: 50, name: "Android", category: "Phones", price: 42.50, image: "/static/assets/phone3.jpg" },
  { id: 31, name: "Jeans", category: "Clothing", price: 72.30, image: "/static/assets/jean.jpg" },
  { id: 12, name: "Earbud", category: "Phones Accessories", price: 67.80, image: "/static/assets/earbud.png" },
  { id: 44, name: "Sneaker", category: "Shoes", price: 9.99, image: "/static/assets/mshoe9.jpg" },
  { id: 28, name: "Iphone", category: "Phones", price: 6.50, image: "/static/assets/iphone1.jpg" },
  { id: 16, name: "Gown", category: "Clothing", price: 45.75, image: "/static/assets/fcloth9.jpg" },
  { id: 59, name: "Tablet", category: "Phones", price: 5.00, image: "/static/assets/tab6.jpg" },
  { id: 8, name: "Earbud", category: "Phones Accessories", price: 7.25, image: "/static/assets/bud4.jpg" },
  { id: 4, name: "Micro board", category: "Electronics", price: 45.75, image: "/static/assets/board3.jpg" },
  { id: 51, name: "phone", category: " Phones", price: 16.00, image: "/static/assets/phone4.jpg" },
  { id: 24, name: "Shoe", category: "Shoes", price: 14.99, image: "/static/assets/fshoe8.jpg" },
  { id: 35, name: "Sneaker", category: "Shoes", price: 200.00, image: "/static/assets/male_s1.jpg" },
  { id: 2, name: "Arduino Board", category: "Electronics", price: 10.96, image: "/static/assets/board.jpg" },
  { id: 45, name: "Sneaker", category: "Shoes", price: 125.00, image: "/static/assets/msmhoe4.jpg" },
  { id: 13, name: "Shirt", category: "Clothing", price: 150.00, image: "/static/assets/fcloth1.jpg" },
  { id: 57, name: "selfie", category: "Phone Accessories", price: 12.00, image: "/static/assets/stand2.jpg" },
  { id: 9, name: "Earbud", category: "Phones Accessories", price: 120.45, image: "/static/assets/bud5.jpg" },
  { id: 60, name: "Tablet", category: "Phones", price: 58.00, image: "/static/assets/tab7.jpg" },
  { id: 49, name: "Android phone", category: "Phones", price: 170.00, image: "/static/assets/phone2.jpg" },
  { id: 1, name: "USB cable", category: "Phones Accessories", price: 9.99, image: "/static/assets/able3.jpg" },
  { id: 18, name: "coperate Shoe", category: "Shoes", price: 10.96, image: "/static/assets/fshoe2.jpg" },
  { id: 20, name: "Female Shoe", category: "Shoes", price: 9.99, image: "/static/assets/fshoe4.jpg" },
  { id: 23, name: "coperate Shoe", category: "Shoes", price: 55.55, image: "/static/assets/fshoe7.jpg" },
  { id: 34, name: "round neck t-shirt", category: "Clothing", price: 50.00, image: "/static/assets/male_c1.jpg" },
  { id: 26, name: "headset", category: "Phone Accessories", price: 19.99, image: "/static/assets/headset2.jpg" },
  { id: 52, name: "Android", category: "Phones", price: 105.00, image: "/static/assets/phone5.jpg" },
  { id: 30, name: "soldering iron", category: "Electronics", price: 25.00, image: "/static/assets/iron.jpg" },
  { id: 11, name: "cord", category: "Phones Accessories", price: 99.99, image: "/static/assets/cord.jpg" },
  { id: 55, name: "sneaker", category: "Shoes", price: 20.00, image: "/static/assets/sneaker1.jpg" },
  { id: 32, name: "Jeans", category: "Clothing", price: 8.99, image: "/static/assets/jean2.jpg" },
  { id: 37, name: "shirt", category: "Clothing", price: 65.00, image: "/static/assets/mcloth5.jpg" },
  { id: 38, name: "shirt", category: "Clothing", price: 18.50, image: "/static/assets/mshirt2.jpg" },
  { id: 40, name: "sneaker", category: "Shoes", price: 4.75, image: "/static/assets/mshoe2.jpg" },
  { id: 41, name: "mem sneaker", category: "Shoes", price: 135.00, image: "/static/assets/mshoe3.jpg" },
  { id: 53, name: "Iphone", category: "Phones", price: 70.99, image: "/static/assets/phone6.jpg" }
];
// Cart storage
let cart = [];

// Function to render categories
function renderCategories() {
    const categoryList = document.getElementById("category-list");
    categoryList.innerHTML = categories.map(category =>
        `<li onclick="filterProducts('${category}')">${category}</li>`
    ).join("");
}

// Function to render products based on category filter
function renderProducts(category = "All") {
    const productList = document.getElementById("product-list");

    // Filter products based on category
    const filteredProducts = category === "All"
        ? products
        : products.filter(product => product.category === category);

    productList.innerHTML = filteredProducts.map(product => `
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
    fetch("/add_to_cart", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ product_id: productId }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message || "Error adding to cart.");
    })
    .catch(error => console.error("Error:", error));
}

// Function to remove a product from the cart
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
        alert(data.message || "Error removing item.");
        location.reload(); // Refresh to update cart
    })
    .catch(error => console.error("Error:", error));
}

// Initialize page content on load
document.addEventListener("DOMContentLoaded", () => {
    renderCategories();
    renderProducts();
});
