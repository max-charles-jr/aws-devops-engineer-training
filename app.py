from flask import Flask, jsonify, render_template, request, session, redirect, url_for
import os
import json
from datetime import datetime
import uuid

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# Sample product data
PRODUCTS = [
    {
        'id': '1',
        'name': 'AWS Certified Solutions Architect Book',
        'category': 'Books',
        'price': 49.99,
        'rating': 4.5,
        'reviews': 1234,
        'image': 'https://via.placeholder.com/200x300/232F3E/FFFFFF?text=AWS+Book',
        'description': 'Complete guide to AWS Solutions Architect certification',
        'in_stock': True
    },
    {
        'id': '2',
        'name': 'Mechanical Keyboard - RGB',
        'category': 'Electronics',
        'price': 129.99,
        'rating': 4.7,
        'reviews': 856,
        'image': 'https://via.placeholder.com/200x300/FF9900/FFFFFF?text=Keyboard',
        'description': 'Professional mechanical keyboard with RGB lighting',
        'in_stock': True
    },
    {
        'id': '3',
        'name': 'Wireless Mouse',
        'category': 'Electronics',
        'price': 29.99,
        'rating': 4.3,
        'reviews': 2341,
        'image': 'https://via.placeholder.com/200x300/146EB4/FFFFFF?text=Mouse',
        'description': 'Ergonomic wireless mouse with precision tracking',
        'in_stock': True
    },
    {
        'id': '4',
        'name': 'Python Programming Guide',
        'category': 'Books',
        'price': 39.99,
        'rating': 4.8,
        'reviews': 3421,
        'image': 'https://via.placeholder.com/200x300/232F3E/FFFFFF?text=Python+Book',
        'description': 'Learn Python programming from basics to advanced',
        'in_stock': True
    },
    {
        'id': '5',
        'name': 'USB-C Hub Adapter',
        'category': 'Electronics',
        'price': 45.99,
        'rating': 4.4,
        'reviews': 678,
        'image': 'https://via.placeholder.com/200x300/FF9900/FFFFFF?text=USB+Hub',
        'description': '7-in-1 USB-C hub with HDMI, USB 3.0, and SD card reader',
        'in_stock': True
    },
    {
        'id': '6',
        'name': 'DevOps Handbook',
        'category': 'Books',
        'price': 44.99,
        'rating': 4.9,
        'reviews': 1876,
        'image': 'https://via.placeholder.com/200x300/232F3E/FFFFFF?text=DevOps+Book',
        'description': 'The definitive guide to DevOps practices and culture',
        'in_stock': True
    },
    {
        'id': '7',
        'name': 'Laptop Stand',
        'category': 'Office',
        'price': 34.99,
        'rating': 4.6,
        'reviews': 1543,
        'image': 'https://via.placeholder.com/200x300/146EB4/FFFFFF?text=Laptop+Stand',
        'description': 'Adjustable aluminum laptop stand for better ergonomics',
        'in_stock': True
    },
    {
        'id': '8',
        'name': 'Noise Cancelling Headphones',
        'category': 'Electronics',
        'price': 199.99,
        'rating': 4.7,
        'reviews': 4532,
        'image': 'https://via.placeholder.com/200x300/FF9900/FFFFFF?text=Headphones',
        'description': 'Premium wireless headphones with active noise cancellation',
        'in_stock': True
    },
    {
        'id': '9',
        'name': 'Desk Organizer Set',
        'category': 'Office',
        'price': 24.99,
        'rating': 4.2,
        'reviews': 892,
        'image': 'https://via.placeholder.com/200x300/146EB4/FFFFFF?text=Organizer',
        'description': 'Complete desk organization system with multiple compartments',
        'in_stock': True
    },
    {
        'id': '10',
        'name': 'Cloud Computing Essentials',
        'category': 'Books',
        'price': 54.99,
        'rating': 4.6,
        'reviews': 967,
        'image': 'https://via.placeholder.com/200x300/232F3E/FFFFFF?text=Cloud+Book',
        'description': 'Master cloud computing concepts and AWS services',
        'in_stock': True
    }
]

@app.route('/')
def home():
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = []
    
    category = request.args.get('category', 'all')
    search = request.args.get('search', '')
    
    filtered_products = PRODUCTS
    
    if category != 'all':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search:
        filtered_products = [p for p in filtered_products if search.lower() in p['name'].lower() or search.lower() in p['description'].lower()]
    
    categories = list(set([p['category'] for p in PRODUCTS]))
    
    return render_template('index.html', 
                         products=filtered_products, 
                         categories=categories,
                         selected_category=category,
                         search_term=search,
                         cart_count=len(session.get('cart', [])))

@app.route('/product/<product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return "Product not found", 404
    
    # Get related products from same category
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != product_id][:4]
    
    return render_template('product_detail.html', 
                         product=product, 
                         related_products=related,
                         cart_count=len(session.get('cart', [])))

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['product_id']), None)
        if product:
            cart_product = product.copy()
            cart_product['quantity'] = item['quantity']
            cart_product['subtotal'] = product['price'] * item['quantity']
            cart_products.append(cart_product)
            total += cart_product['subtotal']
    
    return render_template('cart.html', 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items))

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if 'cart' not in session:
        session['cart'] = []
    
    # Check if product exists
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'success': False, 'message': 'Product not found'}), 404
    
    # Check if item already in cart
    cart = session['cart']
    existing_item = next((item for item in cart if item['product_id'] == product_id), None)
    
    if existing_item:
        existing_item['quantity'] += quantity
    else:
        cart.append({
            'product_id': product_id,
            'quantity': quantity,
            'added_at': datetime.now().isoformat()
        })
    
    session['cart'] = cart
    session.modified = True
    
    return jsonify({
        'success': True, 
        'message': 'Added to cart',
        'cart_count': len(cart)
    })

@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    
    if 'cart' in session:
        session['cart'] = [item for item in session['cart'] if item['product_id'] != product_id]
        session.modified = True
    
    return jsonify({'success': True, 'cart_count': len(session.get('cart', []))})

@app.route('/api/cart/update', methods=['POST'])
def update_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    if 'cart' in session:
        for item in session['cart']:
            if item['product_id'] == product_id:
                item['quantity'] = max(1, quantity)
                break
        session.modified = True
    
    return jsonify({'success': True})

@app.route('/checkout')
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        return redirect(url_for('cart'))
    
    cart_products = []
    total = 0
    
    for item in cart_items:
        product = next((p for p in PRODUCTS if p['id'] == item['product_id']), None)
        if product:
            cart_product = product.copy()
            cart_product['quantity'] = item['quantity']
            cart_product['subtotal'] = product['price'] * item['quantity']
            cart_products.append(cart_product)
            total += cart_product['subtotal']
    
    return render_template('checkout.html', 
                         cart_items=cart_products, 
                         total=total,
                         cart_count=len(cart_items))

@app.route('/api/checkout/process', methods=['POST'])
def process_checkout():
    data = request.get_json()
    
    # Simulate order processing
    order_id = str(uuid.uuid4())[:8].upper()
    
    # Clear cart
    session['cart'] = []
    session.modified = True
    
    return jsonify({
        'success': True,
        'order_id': order_id,
        'message': 'Order placed successfully!'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'ecommerce-app',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/info')
def info():
    return jsonify({
        'application': 'AWS DevOps E-Commerce Demo',
        'environment': os.getenv('ENVIRONMENT', 'development'),
        'version': '2.0.0',
        'features': ['shopping_cart', 'product_catalog', 'checkout', 'search']
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)