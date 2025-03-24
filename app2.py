from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__, static_folder='static')

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce_site5.db'
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
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone_number = request.form.get('phone_number')
        address = request.form.get('address')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash("Email already exists!", "danger")
            return redirect(url_for('register'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            address=address,
            password=password  # No hashing
        )
        db.session.add(new_user)
        db.session.commit()
        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

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
    
    if request.method == 'POST':
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        flash("Checkout complete!", "success")
        return redirect(url_for('home'))

    return render_template('checkout.html')

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
with app.app_context():
    db.create_all()
    if not Product.query.first():
        sample_products = [
            Product(name="Laptop", category="Electronics", price=1200.00, image="headset2.jpg"),
            Product(name="Smartphone", category="Electronics", price=800.00, image="phone.jpg"),
            Product(name="Headphones", category="Accessories", price=150.00, image="headset2.jpg"),
            Product(name="T-shirt", category="Clothing", price=10.00, image="mcloth3.jpg")
        ]
        db.session.add_all(sample_products)
        db.session.commit()
        print("✅ Sample products added to database!")

if __name__ == '__main__':
    app.run(debug=True)
