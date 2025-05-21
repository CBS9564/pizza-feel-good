from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'super_secret_pizza_key'  # Important for session management!

PIZZAS = [
    {'id': 'pepperoni', 'name': 'Pepperoni', 'description': 'Classic pepperoni pizza with a zesty tomato sauce and mozzarella cheese.', 'price': 12.99},
    {'id': 'margherita', 'name': 'Margherita', 'description': 'Simple yet delicious pizza with fresh mozzarella, basil, and tomato.', 'price': 10.99},
    {'id': 'veggie', 'name': 'Veggie Supreme', 'description': 'A delightful mix of fresh vegetables including bell peppers, onions, olives, and mushrooms.', 'price': 11.99},
    {'id': 'hawaiian', 'name': 'Hawaiian', 'description': 'A controversial classic with ham, pineapple, and mozzarella cheese.', 'price': 13.49}
]

@app.route('/')
def index():
    return render_template('index.html', pizzas=PIZZAS)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        phone = request.form.get('phone')
        pizza_id = request.form.get('pizza_id')
        
        selected_pizza = next((pizza for pizza in PIZZAS if pizza['id'] == pizza_id), None)
        
        if selected_pizza:
            session['order_details'] = {
                'name': name,
                'address': address,
                'phone': phone,
                'pizza_name': selected_pizza['name'],
                'pizza_price': selected_pizza['price']
            }
            print(f"Order details stored in session: {session['order_details']}") # For debugging
        else:
            # Handle case where pizza_id is invalid, though form validation should prevent this
            print(f"Invalid pizza_id received: {pizza_id}")
            # You might want to redirect back to order form with an error message
            return redirect(url_for('order')) 
            
        return redirect(url_for('order_confirmation'))
    
    return render_template('order.html', pizzas=PIZZAS)

@app.route('/order_confirmation')
def order_confirmation():
    details = session.get('order_details', {})
    print(f"Retrieved details from session for confirmation: {details}") # For debugging
    return render_template('order_confirmation.html', details=details)

if __name__ == '__main__':
    app.run(debug=True)
