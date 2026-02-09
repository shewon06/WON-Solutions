from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Sale, SaleItem, Expense, Product
from datetime import datetime, date
from sqlalchemy import func

reports = Blueprint('reports', __name__)

@reports.route('/reports')
@login_required
def report_dashboard():
    # Summary Stats
    from datetime import datetime as dt
    today_start = dt.combine(date.today(), dt.min.time())
    today_end = dt.combine(date.today(), dt.max.time())
    
    sales_today = Sale.objects(created_at__gte=today_start, created_at__lte=today_end).sum('total_amount')
    expenses_today = Expense.objects(created_at__gte=today_start, created_at__lte=today_end).sum('amount')
    
    # Recent Sales
    recent_sales = Sale.objects().order_by('-created_at').limit(10)
    
    # Financial Overview (Simplified)
    total_inventory_value = sum(p.stock_qty * p.cost_price for p in Product.objects())
    
    return render_template('reports/dashboard.html', 
                           sales_today=sales_today, 
                           expenses_today=expenses_today,
                           recent_sales=recent_sales,
                           total_inventory_value=total_inventory_value,
                           now=datetime.now())

@reports.route('/expenses', methods=['GET', 'POST'])
@login_required
def browse_expenses():
    if request.method == 'POST':
        desc = request.form.get('description')
        amount = float(request.form.get('amount', 0))
        vat_amount = float(request.form.get('vat_amount', 0))
        cat = request.form.get('category')
        exp_date_str = request.form.get('expense_date', date.today().isoformat())
        exp_date = datetime.strptime(exp_date_str, '%Y-%m-%d').date()
        
        new_expense = Expense(
            description=desc, 
            amount=amount, 
            vat_amount=vat_amount, 
            category=cat,
            expense_date=exp_date if isinstance(exp_date, dt) else dt.combine(exp_date, dt.min.time())
        )
        new_expense.save()
        flash('Expense recorded successfully!', 'success')
        return redirect(url_for('reports.browse_expenses'))
    
    expenses = Expense.objects().order_by('-created_at')
    return render_template('reports/expenses.html', expenses=expenses, today_date=date.today().isoformat())
