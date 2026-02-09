from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import db, Customer, Supplier
import csv
import io
import requests

crm = Blueprint('crm', __name__)

@crm.route('/customers/upload', methods=['POST'])
@login_required
def upload_customers():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('crm.manage_customers'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('crm.manage_customers'))
    
    if file and file.filename.endswith('.csv'):
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_input = csv.DictReader(stream)
        
        count = 0
        for row in csv_input:
            name = row.get('name')
            phone = row.get('phone')
            address = row.get('address')
            
            if name:
                # Basic duplicate check
                existing = Customer.objects(phone=phone).first() if phone else None
                if not existing:
                    new_cust = Customer(name=name, phone=phone, address=address)
                    new_cust.save()
                    count += 1
        
        flash(f'Successfully imported {count} customers!', 'success')
    else:
        flash('Please upload a CSV file.', 'danger')
        
    return redirect(url_for('crm.manage_customers'))

@crm.route('/customers/sync', methods=['POST'])
@login_required
def sync_from_website():
    api_url = request.form.get('api_url')
    if not api_url:
        flash('API URL is required.', 'danger')
        return redirect(url_for('crm.manage_customers'))
    
    try:
        response = requests.get(api_url, timeout=10)
        data = response.json()
        
        count = 0
        # Expected format: [{"name": "...", "phone": "...", "address": "..."}, ...]
        for item in data:
            name = item.get('name')
            phone = item.get('phone')
            address = item.get('address')
            
            if name:
                existing = Customer.objects(phone=phone).first() if phone else None
                if not existing:
                    new_cust = Customer(name=name, phone=phone, address=address)
                    new_cust.save()
                    count += 1
        
        flash(f'Successfully synced {count} customers from website!', 'success')
    except Exception as e:
        flash(f'Sync failed: {str(e)}', 'danger')
        
    return redirect(url_for('crm.manage_customers'))

@crm.route('/customers', methods=['GET', 'POST'])
@login_required
def manage_customers():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            phone = request.form.get('phone')
            address = request.form.get('address')
            
            # Critical: Check for duplicates
            if phone:
                existing = Customer.objects(phone=phone).first()
                if existing:
                    flash(f'Error: Customer with phone {phone} already exists!', 'danger')
                    return redirect(url_for('crm.manage_customers'))

            new_customer = Customer(name=name, phone=phone, address=address)
            new_customer.save()
            flash(f'Customer {name} added successfully!', 'success')
        except Exception as e:
            flash(f'Error adding customer: {str(e)}', 'danger')
        return redirect(url_for('crm.manage_customers'))
    
    customers = Customer.objects()
    return render_template('crm/customers.html', customers=customers)

@crm.route('/suppliers', methods=['GET', 'POST'])
@login_required
def manage_suppliers():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        
        new_supplier = Supplier(name=name, phone=phone)
        new_supplier.save()
        flash(f'Supplier {name} added successfully!', 'success')
        return redirect(url_for('crm.manage_suppliers'))
    
    suppliers = Supplier.objects()
    return render_template('crm/suppliers.html', suppliers=suppliers)
