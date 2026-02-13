from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required
from models import db, Product, Category, Supplier, CompanyMaster
from utils.importers import import_daraz_products, process_daraz_items
from utils.daraz_client import DarazClient
import os

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

@inventory.route('/inventory/import/daraz', methods=['POST'])
@login_required
def import_daraz():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('inventory.list_products'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('inventory.list_products'))
    
    if file:
        file_extension = os.path.splitext(file.filename)[1]
        file_data = file.read()
        
        result = import_daraz_products(file_data, file_extension)
        
        if result['success']:
            flash(result.get('message', 'Import Successful'), 'success')
        else:
            flash(f"Import Failed: {result['message']}", 'danger')
            
    return redirect(url_for('inventory.list_products'))

@inventory.route('/inventory/sync-daraz', methods=['POST'])
@login_required
def sync_daraz():
    settings = CompanyMaster.objects().first()
    if not settings or not settings.daraz_app_key or not settings.daraz_app_secret:
        flash('Daraz API credentials not configured in Settings.', 'warning')
        return redirect(url_for('inventory.list_products'))

    if not settings.daraz_access_token:
        flash('Daraz is not connected. Please authorize in Settings.', 'warning')
        return redirect(url_for('inventory.list_products'))

    client = DarazClient(settings.daraz_app_key, settings.daraz_app_secret, settings.daraz_access_token)
    
    # Fetch first page of products
    response = client.get_products(limit=50)
    
    if response.get('code') != '0':
        # Check if token expired (Daraz usually returns specific code for this)
        if response.get('code') in ['IllegalAccessToken', 'AccessTokenExpired']:
            flash('Daraz access token expired. Please re-connect in Settings.', 'danger')
        else:
            flash(f"Sync Failed: {response.get('message', 'Unknown API Error')}", 'danger')
        return redirect(url_for('inventory.list_products'))

    daraz_products = response.get('data', {}).get('products', [])
    items_to_process = []
    
    for p in daraz_products:
        name = p.get('attributes', {}).get('name')
        category = p.get('attributes', {}).get('category')
        
        for sku_info in p.get('skus', []):
            items_to_process.append({
                'sku': sku_info.get('SellerSku'),
                'name': name,
                'price': sku_info.get('price'),
                'qty': sku_info.get('quantity'),
                'category_name': category
            })

    if items_to_process:
        result = process_daraz_items(items_to_process)
        flash(f"Sync Complete: {result['imported']} new products added, {result['updated']} updated.", 'success')
    else:
        flash("No products found in Daraz Seller Center.", 'info')

    return redirect(url_for('inventory.list_products'))
