# E-commerce API

This is a Flask-based RESTful API for managing e-commerce operations like managing customers, products, orders, and customer accounts.

## Installation

1. Clone this repository:
https://github.com/ejones001/my-coding-temple-flask-e-commerce-api


2. Navigate to the project directory:

E-commerce-api


3. Install dependencies:


4. Set up your MySQL database and configure the connection string in `app.py`.

5. Run the Flask app:


6. The API should now be accessible at `http://localhost:5000`.

## Usage

- Create a new customer: `POST /customers/`
- Get a customer by ID: `GET /customers/<id>`
- Update a customer by ID: `PUT /customers/<id>`
- Delete a customer by ID: `DELETE /customers/<id>`

- Create a new customer account: `POST /customer_account/`
- Get a customer account by ID: `GET /customer_account/<id>`
- Update a customer account by ID: `PUT /customer_account/<id>`
- Delete a customer account by ID: `DELETE /customer_account/<id>`

- Create a new product: `POST /products/`
- Get a product by ID: `GET /products/<id>`
- Update a product by ID: `PUT /products/<id>`
- Delete a product by ID: `DELETE /products/<id>`
- List all products: `GET /products/`

- Place a new order: `POST /orders/`
- Get an order by ID: `GET /orders/<id>`
- List all orders: `GET /orders/`

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- MySQL Connector

## Contributing

Contributions are welcome! Please feel free to submit any issues or pull requests.



