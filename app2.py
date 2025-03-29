from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce_site7.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(100), nullable=False)  # No hashing

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)

# Product Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False, default="Uncategorized")
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=True, default="default.jpg")

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete="CASCADE"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route - Display Products
@app.route('/')
def home():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)  # Debugging Step 1
        
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        password = request.form.get('password')

        if not first_name or not last_name or not email or not phone_number or not address or not password:
            flash("All fields are required!", "danger")
            return redirect(url_for('register'))
        
        print("Form Data Received")  # Debugging Step 2

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password
        )
        db.session.add(new_user)

        try:
            db.session.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            print(f"Database Error: {e}")  # Debugging Step 3
            flash("An error occurred while saving your data.", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')


# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid email or password!", "danger")

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", "info")
    return redirect(url_for('home'))

# Add Product to Cart
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product does not exist"}), 404

    if current_user.is_authenticated:
        existing_cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if existing_cart_item:
            existing_cart_item.quantity += 1
        else:
            new_cart_item = Cart(user_id=current_user.id, product_id=product_id, quantity=1)
            db.session.add(new_cart_item)
        db.session.commit()
    else:
        if "cart" not in session:
            session["cart"] = []
        cart = session["cart"]
        found = False
        for item in cart:
            if item["product_id"] == product_id:
                item["quantity"] += 1
                found = True
                break
        if not found:
            cart.append({
                "product_id": product_id,
                "product_name": product.name,
                "product_price": product.price,
                "product_image": product.image,
                "quantity": 1
            })
        session["cart"] = cart

    return jsonify({"message": "Product added to cart!"}), 201

# View Cart
@app.route('/cart')
def cart():
    cart_items = []

    if current_user.is_authenticated:
        user_cart = Cart.query.filter_by(user_id=current_user.id).all()
        cart_items += [{
            "id": c.id,
            "product_id": c.product_id,
            "product_name": c.product.name,
            "product_price": c.product.price,
            "product_image": c.product.image,
            "quantity": c.quantity
        } for c in user_cart if c.product]

    if "cart" in session:
        cart_items += session["cart"]

    return render_template('cart.html', cart_items=cart_items)

# Checkout Route
@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', [])  # Assuming you're storing cart in session
    total_amount = sum(item['product_price'] * item['quantity'] for item in cart_items)

    if request.method == 'POST':
        # Process payment or order completion logic here
        session['cart'] = []  # Clear the cart after successful checkout
        return jsonify({"message": "Checkout complete!"})

    return render_template('checkout.html', cart_items=cart_items, total_amount=total_amount)


@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = data.get("product_id")

    if not product_id:
        return jsonify({"error": "Product ID is required"}), 400

    if current_user.is_authenticated:
        cart_item = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({"message": "Product removed from cart!"}), 200
        else:
            return jsonify({"error": "Product not found in cart!"}), 404
    else:
        if "cart" in session:
            session["cart"] = [item for item in session["cart"] if item["product_id"] != product_id]
            return jsonify({"message": "Product removed from cart!"}), 200

    return jsonify({"error": "Something went wrong"}), 500

# Check If User is Logged In
@app.route("/is_logged_in")
def is_logged_in():
    return jsonify({"logged_in": current_user.is_authenticated})

# Initialize Database
# Initialize Database
with app.app_context():
    db.create_all()

    # Check if database is empty before adding products
    if not Product.query.first():
        sample_products = [
            Product(name="Laptop", category="Electronics", price=1200.00, image="headset2.jpg"),
            Product(name="Smartphone", category="Electronics", price=800.00, image="phone.jpg"),
            Product(name="Headphones", category="Accessories", price=150.00, image="headset2.jpg"),
            Product(name="T-shirt", category="Clothing", price=10.00, image="mcloth3.jpg"),
            Product(name="T-shirt", category="Clothing", price=10.00, image="mcloth4.jpg")
        ]
        
        # New products
        new_products = [
            Product(name="Ipad", category="Phones", price=110.00, image="ipad1.jpg"),
            Product(name="Unisex shirt", category="Clothing", price=89.99, image="fcloth4.jpg"),
            Product(name="White canvas", category="Shoes", price=30.00, image="mshoe5.jpg"),
            Product(name="Earbud", category="Phones Accessories", price=15.75, image="bud.jpg"),
            Product(name="Plain t-shirt", category="Clothing", price=140.50, image="m1.jpg"),
            Product(name="Android", category="Phones", price=156.99, image="phone.png"),
            Product(name="Female Casual Shoe", category="Shoes", price=180.20, image="fshoe5.jpg"),
            Product(name="Charger", category="Phones Accessories", price=5.60, image="charger.jpg"),
            Product(name="Android", category="Phones", price=145.00, image="phone7.jpg"),
            Product(name="Arduino Board", category="Electronics", price=12.50, image="board2.jpg"),
            Product(name="Female Shoe", category="Shoes", price=12.50, image="fshoe3.jpg"),
            Product(name="Selfie Stick", category="Phone Accessories", price=190.00, image="stand3.jpg"),
            Product(name="T-shirt", category="Clothing", price=10.00, image="mcloth3.jpg"),
            Product(name="Ipad", category="Phones", price=600.00, image="pad4.jpg"),
            Product(name="Casual Shoe", category="Shoes", price=2.99, image="fshoe6.jpg"),
            Product(name="Sensor", category="Electronics", price=22.40, image="board4.jpg"),
            Product(name="Gown", category="Clothing", price=3.25, image="fcloth3.jpg"),
            Product(name="Phone Stand", category="Phone Accessories", price=80.00, image="stand1.jpg"),
            Product(name="D-bass", category="Phone Accessories", price=75.00, image="headset.png"),
            Product(name="Sneaker", category="Shoes", price=88.88, image="mshoe1.jpg"),
            Product(name="Ipad", category="Phones", price=350.00, image="pad3.jpg"),
            Product(name="Iphone", category="Phones", price=160.25, image="iphone2.jpg"),
            Product(name="Earbud", category="Phones Accessories", price=33.33, image="bud2.jpg"),
            Product(name="Canvas", category="Shoes", price=77.77, image="mshoe7.jpg"),
            Product(name="Shoe", category="Shoes", price=22.40, image="fshoe1.jpg"),
            Product(name="Android", category="Phones", price=42.50, image="phone3.jpg"),
            Product(name="Jeans", category="Clothing", price=72.30, image="jean.jpg"),
            Product(name="Earbud", category="Phones Accessories", price=67.80, image="earbud.png"),
            Product(name="Sneaker", category="Shoes", price=9.99, image="mshoe9.jpg"),
            Product(name="Iphone", category="Phones", price=6.50, image="iphone1.jpg"),
            Product(name="Gown", category="Clothing", price=45.75, image="fcloth9.jpg"),
            Product(name="Tablet", category="Phones", price=5.00, image="tab6.jpg"),
            Product(name="Earbud", category="Phones Accessories", price=7.25, image="bud4.jpg"),
            Product(name="Micro board", category="Electronics", price=45.75, image="board3.jpg"),
            Product(name="Phone", category="Phones", price=16.00, image="phone4.jpg"),
            Product(name="Shoe", category="Shoes", price=14.99, image="fshoe8.jpg"),
            Product(name="Sneaker", category="Shoes", price=200.00, image="male_s1.jpg"),
            Product(name="Arduino Board", category="Electronics", price=10.96, image="board.jpg"),
            Product(name="Sneaker", category="Shoes", price=125.00, image="msmhoe4.jpg"),
            Product(name="Shirt", category="Clothing", price=150.00, image="fcloth1.jpg"),
            Product(name="Selfie", category="Phone Accessories", price=12.00, image="stand2.jpg"),
            Product(name="Earbud", category="Phones Accessories", price=120.45, image="bud5.jpg"),
            Product(name="Tablet", category="Phones", price=58.00, image="tab7.jpg"),
            Product(name="Android Phone", category="Phones", price=170.00, image="phone2.jpg"),
            Product(name="USB Cable", category="Phones Accessories", price=9.99, image="able3.jpg"),
            Product(name="Corporate Shoe", category="Shoes", price=10.96, image="fshoe2.jpg"),
            Product(name="Female Shoe", category="Shoes", price=9.99, image="fshoe4.jpg"),
            Product(name="Corporate Shoe", category="Shoes", price=55.55, image="fshoe7.jpg"),
            Product(name="Round Neck T-shirt", category="Clothing", price=50.00, image="male_c1.jpg"),
            Product(name="Headset", category="Phone Accessories", price=19.99, image="headset2.jpg"),
            Product(name="Android", category="Phones", price=105.00, image="phone5.jpg"),
            Product(name="Soldering Iron", category="Electronics", price=25.00, image="iron.jpg"),
            Product(name="Cord", category="Phones Accessories", price=99.99, image="cord.jpg"),
            Product(name="Sneaker", category="Shoes", price=20.00, image="sneaker1.jpg"),
            Product(name="Jeans", category="Clothing", price=8.99, image="jean2.jpg"),
            Product(name="Shirt", category="Clothing", price=65.00, image="mcloth5.jpg"),
            Product(name="Shirt", category="Clothing", price=18.50, image="mshirt2.jpg"),
            Product(name="Sneaker", category="Shoes", price=4.75, image="mshoe2.jpg"),
            Product(name="Men's Sneaker", category="Shoes", price=135.00, image="mshoe3.jpg"),
            Product(name="Iphone", category="Phones", price=70.99, image="phone6.jpg")
        ]

        # Add new products
        db.session.add_all(sample_products + new_products)
        db.session.commit()
        print("✅ Sample products added to database!")


if __name__ == '__main__':
    app.run(debug=True)
