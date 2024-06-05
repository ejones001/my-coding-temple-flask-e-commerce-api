from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from urllib.parse import quote_plus

app = Flask(__name__)
pw = 'That08er'
encoded_pw = quote_plus(pw)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{encoded_pw}@localhost/e_commerce_api'
db = SQLAlchemy(app)
ma = Marshmallow(app)



# Models
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))

class CustomerAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    customer = db.relationship('Customer', backref=db.backref('account', uselist=False))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    customer = db.relationship('Customer', backref=db.backref('orders', lazy=True))

# Schemas
from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class CustomerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Customer

class CustomerAccountSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CustomerAccount

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
customer_account_schema = CustomerAccountSchema()
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)

# Routes
app.route('/')
def home():
    return 'Welcome to the E commerce Api program'

@app.route('/customers/', methods=['POST'])
def create_customer():
    data = request.get_json()
    new_customer = Customer(
        name=data['name'],
        email=data['email'],
        phone_number=data.get('phone_number')
    )
    db.session.add(new_customer)
    db.session.commit()
    return customer_schema.jsonify(new_customer), 201

@app.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    customer.name = data['name']
    customer.email = data['email']
    customer.phone_number = data.get('phone_number')
    db.session.commit()
    return customer_schema.jsonify(customer)

@app.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    db.session.delete(customer)
    db.session.commit()
    return '', 204

@app.route('/customer_account/', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    new_account = CustomerAccount(
        username=data['username'],
        customer_id=data['customer_id']
    )
    db.session.add(new_account)
    db.session.commit()
    return customer_account_schema.jsonify(new_account), 201

@app.route('/customer_account/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return customer_account_schema.jsonify(account)

@app.route('/customer_account/<int:id>', methods=['PUT'])
def update_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    data = request.get_json()
    account.username = data['username']
    db.session.commit()
    return customer_account_schema.jsonify(account)

@app.route('/customer_account/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    db.session.delete(account)
    db.session.commit()
    return '', 204

@app.route('/products/', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        stock=data.get('stock', 0)
    )
    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product), 201

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    product.name = data['name']
    product.price = data['price']
    product.stock = data.get('stock', product.stock)
    db.session.commit()
    return product_schema.jsonify(product)

@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return '', 204

@app.route('/products/', methods=['GET'])
def list_products():
    products = Product.query.all()
    return products_schema.jsonify(products)

@app.route('/orders/', methods=['POST'])
def place_order():
    data = request.get_json()
    new_order = Order(
        customer_id=data['customer_id'],
        order_date=data.get('order_date', db.func.current_timestamp())
    )
    db.session.add(new_order)
    db.session.commit()
    return order_schema.jsonify(new_order), 201

@app.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return order_schema.jsonify(order)

@app.route('/orders/', methods=['GET'])
def list_orders():
    orders = Order.query.all()
    return orders_schema.jsonify(orders)

if __name__ == '__main__':
    app.run(debug=True)
