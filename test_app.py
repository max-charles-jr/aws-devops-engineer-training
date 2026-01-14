import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test the home page loads successfully"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'DevOps Shop' in response.data

def test_health_endpoint(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['status'] == 'healthy'
    assert json_data['version'] == '2.0.0'

def test_info_endpoint(client):
    """Test the info API endpoint"""
    response = client.get('/api/info')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['application'] == 'AWS DevOps E-Commerce Demo'
    assert 'shopping_cart' in json_data['features']

def test_product_detail(client):
    """Test product detail page"""
    response = client.get('/product/1')
    assert response.status_code == 200
    assert b'AWS Certified Solutions Architect Book' in response.data

def test_add_to_cart(client):
    """Test adding product to cart"""
    response = client.post('/api/cart/add',
                          data=json.dumps({'product_id': '1', 'quantity': 1}),
                          content_type='application/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] == True
    assert json_data['cart_count'] == 1

def test_cart_page(client):
    """Test cart page"""
    # Add item to cart first
    with client.session_transaction() as sess:
        sess['cart'] = [{'product_id': '1', 'quantity': 2}]
    
    response = client.get('/cart')
    assert response.status_code == 200
    assert b'Shopping Cart' in response.data

def test_remove_from_cart(client):
    """Test removing product from cart"""
    # Add item to cart first
    with client.session_transaction() as sess:
        sess['cart'] = [{'product_id': '1', 'quantity': 1}]
    
    response = client.post('/api/cart/remove',
                          data=json.dumps({'product_id': '1'}),
                          content_type='application/json')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] == True
    assert json_data['cart_count'] == 0

def test_search_functionality(client):
    """Test product search"""
    response = client.get('/?search=AWS')
    assert response.status_code == 200
    assert b'AWS' in response.data

def test_category_filter(client):
    """Test category filtering"""
    response = client.get('/?category=Books')
    assert response.status_code == 200
    assert b'Books' in response.data

def test_checkout_page(client):
    """Test checkout page with items in cart"""
    with client.session_transaction() as sess:
        sess['cart'] = [{'product_id': '1', 'quantity': 1}]
    
    response = client.get('/checkout')
    assert response.status_code == 200
    assert b'Checkout' in response.data

def test_checkout_empty_cart_redirect(client):
    """Test checkout redirects when cart is empty"""
    response = client.get('/checkout')
    assert response.status_code == 302  # Redirect