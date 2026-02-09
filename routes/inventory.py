from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import db, Product, Category, Supplier

inventory = Blueprint('inventory', __name__)

@inventory.route('/inventory')
@login_required
def list_products():
    products = Product.objects()
    categories = Category.objects()
    suppliers = Supplier.objects()
    return render_template('inventory/list.html', products=products, categories=categories, suppliers=suppliers)

@inventory.route('/inventory/add', methods=['POST'])
@login_required
def add_product():
    try:
        name = request.form.get('name')
        sku = request.form.get('sku')
        barcode = request.form.get('barcode')
        category_id = request.form.get('category_id')
        cost_price = float(request.form.get('cost_price', 0))
        selling_price = float(request.form.get('selling_price', 0))
        stock_qty = int(request.form.get('stock_qty', 0))
        supplier_id = request.form.get('supplier_id')

        # Critical: Check for duplicates
        if sku:
            existing_sku = Product.objects(sku=sku).first()
            if existing_sku:
                flash(f'Error: SKU {sku} already exists!', 'danger')
                return redirect(url_for('inventory.list_products'))
        
        if barcode:
            existing_barcode = Product.objects(barcode=barcode).first()
            if existing_barcode:
                flash(f'Error: Barcode {barcode} already exists!', 'danger')
                return redirect(url_for('inventory.list_products'))

        new_product = Product(
            name=name, sku=sku, barcode=barcode, category=category_id if category_id else None,
            cost_price=cost_price, selling_price=selling_price, stock_qty=stock_qty,
            supplier=supplier_id if supplier_id else None
        )
        new_product.save()
        flash(f'Product {name} added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding product: {str(e)}', 'danger')
        
    return redirect(url_for('inventory.list_products'))

@inventory.route('/inventory/update_stock/<id>', methods=['POST'])
@login_required
def update_stock(id):
    product = Product.objects.get_or_404(pk=id)
    adjustment = int(request.form.get('adjustment', 0))
    new_cost = request.form.get('cost_price')
    supplier_id = request.form.get('supplier_id')
    
    product.stock_qty += adjustment
    if new_cost:
        product.cost_price = float(new_cost)
    if supplier_id:
        product.supplier = supplier_id
        
    product.save()
    flash(f'Stock updated for {product.name}', 'success')
    return redirect(url_for('inventory.list_products'))
