from flask import Flask, jsonify, request,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root22@localhost:5432/pizza_delivery'

# Suppress SQLAlchemy deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the PizzaOrder model
class PizzaOrder(db.Model):
    __tablename__ = 'pizza_orders'

    id = db.Column(db.Integer, primary_key=True)
    pizza_name = db.Column(db.String(100))
    quantity = db.Column(db.Integer)
    status = db.Column(db.String(50))

# API endpoints
''
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        data = request.get_json()
        pizza_name = data.get('pizza_name')
        quantity = int(data.get('quantity'))

    
        if quantity <= 0:
            raise ValueError('Quantity should be greater than 0.')
    
    # Create a new PizzaOrder instance
        new_order = PizzaOrder(pizza_name=pizza_name, quantity=quantity, status='pending')
        
        # Add the order to the database
        db.session.add(new_order)
        db.session.commit()
    
        return jsonify({'message': 'Order placed successfully','order_id': new_order.id})
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal Server Error'}), 500
    

@app.route('/order_status/<order_id>', methods=['GET'])
def order_status(order_id):
    order = PizzaOrder.query.filter_by(id=order_id).first()
    
    if order:
        return jsonify({'order_status': order.status,'order_id': order.id})
    
    else:
        return jsonify({'message': 'Order not found'})

@app.route('/update_delivery_status/<order_id>', methods=['PUT'])
def update_delivery_status(order_id):
    order = PizzaOrder.query.filter_by(id=order_id).first()
    
    if order:
        order.status = 'delivered'
        db.session.commit()
        return jsonify({'message': 'Order status updated successfully'})
    else:
        return jsonify({'message': 'Order not found'})

if __name__ == '__main__':
    with app.app_context():
        # Create the tables in the database
        db.create_all()
    app.run(debug=True)

# usage
# http://127.0.0.1:5000/place_order

# {
#     "pizza_name": "choose pizza name", 
# (options are Margherita,Farmhouse,Onion Cheeze,Chicken Pizza,Veg Pizza)
#     "quantity": 2
# }

# http://127.0.0.1:5000/order_status/id

# http://127.0.0.1:5000/update_delivery_status/id

