from flask import Flask, render_template, jsonify, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder='static')

# Database configuration (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200), nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)  # New quantity field

    user = db.relationship('User', backref=db.backref('cart', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart', lazy=True))

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    products = Product.query.all()
    if not products:
        return jsonify([])  # Ensure empty list is returned instead of None

    product_list = [{"id": p.id, "name": p.name, "price": p.price, "image": p.image} for p in products]
    return jsonify(product_list)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        product_id = data.get('product_id')

        if not user_id or not product_id:
            return jsonify({"error": "User ID and Product ID are required"}), 400

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
        if cart_item:
            cart_item.quantity += 1  # Increment quantity if already exists
        else:
            cart_item = Cart(user_id=user_id, product_id=product_id, quantity=1)
            db.session.add(cart_item)
        
        db.session.commit()
        return jsonify({"message": "Product added to cart"}), 201

    # Fetch cart items with product details
    cart_items = Cart.query.all()
    cart_data = [{
        "id": c.id,
        "user_id": c.user_id,
        "product": {
            "id": c.product.id,
            "name": c.product.name,
            "price": c.product.price,
            "image": c.product.image
        },
        "quantity": c.quantity
    } for c in cart_items]

    return jsonify(cart_data)

@app.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    
    return jsonify({"message": "Checkout complete!"})

# Initialize database
with app.app_context():
    db.create_all()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
