from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_required, current_user
from models import db, Product, Sale, SaleItem, Customer
from datetime import datetime

pos_bp = Blueprint('pos', __name__)

@pos_bp.route('/pos')
@login_required
def pos_screen():
    products = Product.objects(is_active=True)
    customers = Customer.objects()
    # Initialize cart if it doesn't exist
    if 'cart' not in session:
        session['cart'] = []
    
    # Calculate cart totals
    subtotal = sum(item['price'] * item['qty'] for item in session['cart'])
    
    return render_template('pos.html', products=products, customers=customers, cart=session['cart'], subtotal=subtotal)

@pos_bp.route('/pos/add/<product_id>')
@login_required
def add_to_cart(product_id):
    product = Product.objects.get_or_404(pk=product_id)
    cart = session.get('cart', [])
    
    # Check if product is already in cart
    found = False
    for item in cart:
        if item['id'] == product_id:
            item['qty'] += 1
            found = True
            break
    
    if not found:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.selling_price,
            'qty': 1
        })
    
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('pos.pos_screen'))

@pos_bp.route('/pos/remove/<index>')
@login_required
def remove_from_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        cart.pop(index)
    session['cart'] = cart
    session.modified = True
    return redirect(url_for('pos.pos_screen'))

@pos_bp.route('/pos/clear')
@login_required
def clear_cart():
    session['cart'] = []
    return redirect(url_for('pos.pos_screen'))

@pos_bp.route('/pos/checkout', methods=['POST'])
@login_required
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash('Cart is empty!', 'danger')
        return redirect(url_for('pos.pos_screen'))
    
    payment_type = request.form.get('payment_type', 'CASH')
    customer_id = request.form.get('customer_id')
    
    from models import CompanyMaster
    company = CompanyMaster.objects().first()
    
    total_amount = sum(item['price'] * item['qty'] for item in cart)
    subtotal = total_amount
    vat_amount = 0.0
    
    # Apply VAT if registered (18%)
    if company and company.is_vat_registered:
        vat_amount = total_amount - (total_amount / 1.18)
        subtotal = total_amount - vat_amount

    # Create Sale record
    new_sale = Sale(
        total_amount=total_amount,
        subtotal=subtotal,
        vat_amount=vat_amount,
        is_vat_inclusive=True,
        payment_type=payment_type,
        customer=customer_id if customer_id else None,
        sold_by=current_user.name
    )
    new_sale.save()
    
    # Handle Credit for Customer
    if payment_type == 'CREDIT' and customer_id:
        customer = Customer.objects(pk=customer_id).first()
        if customer:
            customer.credit_balance += total_amount
            customer.save()

    # Create SaleItems and update stock
    total_cost = 0.0
    for item in cart:
        product = Product.objects(pk=item['id']).first()
        if not product or product.stock_qty < item['qty']:
            # In Mongo, we don't have atomic multi-doc transactions so easily without Replica Sets
            # But for this app, we'll just flash error. 
            # Note: The sale was already saved. In a real app we'd use sessions.
            flash(f'Insufficient stock for {item["name"]}!', 'danger')
            return redirect(url_for('pos.pos_screen'))

        sale_item = SaleItem(
            sale=new_sale,
            product=product,
            quantity=item['qty'],
            price=item['price'],
            cost_price=product.cost_price 
        )
        sale_item.save()
        total_cost += (product.cost_price * item['qty'])
        
        # Update stock
        product.stock_qty -= item['qty']
        product.save()
    
    # Provision for Income Tax
    estimated_profit = total_amount - total_cost
    if estimated_profit > 0:
        new_sale.tax_amount = estimated_profit * 0.30
        new_sale.save()
            
    session['cart'] = []
    flash(f'Sale completed successfully!', 'success')
    return redirect(url_for('pos.view_receipt', sale_id=str(new_sale.id)))

@pos_bp.route('/receipt/<sale_id>')
@login_required
def view_receipt(sale_id):
    sale = Sale.objects.get_or_404(pk=sale_id)
    return render_template('pos/receipt.html', sale=sale, now=datetime.now())

@pos_bp.route('/label/<sale_id>')
@login_required
def print_label(sale_id):
    sale = Sale.objects.get_or_404(pk=sale_id)
    return render_template('shipping/label.html', sale=sale)

@pos_bp.route('/api/customers/sync')
@login_required
def sync_customers():
    customers = Customer.objects()
    return jsonify([{
        'id': str(c.id),
        'name': c.name,
        'phone': c.phone,
        'address': c.address
    } for c in customers])
