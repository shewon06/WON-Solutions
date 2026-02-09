from flask import Blueprint, render_template, request
from flask_login import login_required
from models import db, Sale, Expense, Product
from datetime import datetime, date, timedelta
from sqlalchemy import func

financials = Blueprint('financials', __name__)

@financials.route('/reports/daily-summary')
@login_required
def daily_summary():
    from datetime import datetime as dt
    target_start = dt.combine(target_date, dt.min.time())
    target_end = dt.combine(target_date, dt.max.time())
    
    # Sales for the day
    sales = Sale.objects(created_at__gte=target_start, created_at__lte=target_end)
    total_sales = sum(s.total_amount for s in sales)
    
    # Expenses for the day
    expenses = Expense.objects(created_at__gte=target_start, created_at__lte=target_end)
    total_expenses = sum(e.amount for e in expenses)
    
    # Net Profit
    net_profit = total_sales - total_expenses
    
    return render_template('reports/daily_summary.html', 
                           target_date=target_date,
                           sales=sales,
                           total_sales=total_sales,
                           expenses=expenses,
                           total_expenses=total_expenses,
                           net_profit=net_profit)

@financials.route('/reports/p-and-l')
@login_required
def profit_and_loss():
    # Month-to-date summary
    from datetime import datetime as dt
    start_of_month_dt = dt.combine(start_of_month, dt.min.time())
    
    sales_mtd_total = Sale.objects(created_at__gte=start_of_month_dt).sum('total_amount')
    vat_collected_mtd = Sale.objects(created_at__gte=start_of_month_dt).sum('vat_amount')
    
    # Revenue is total sales minus VAT (if VAT inclusive)
    revenue_mtd = sales_mtd_total - vat_collected_mtd
    
    expenses_mtd_total = Expense.objects(created_at__gte=start_of_month_dt).sum('amount')
    vat_paid_mtd = Expense.objects(created_at__gte=start_of_month_dt).sum('vat_amount')
    
    # Operational Expenses minus VAT
    op_expenses_mtd = expenses_mtd_total - vat_paid_mtd
    
    # COGS
    from models import SaleItem
    # In Mongo, we get the sales first, then the items linked to them
    recent_sales_ids = Sale.objects(created_at__gte=start_of_month_dt).scalar('id')
    cogs_mtd = sum(item.quantity * item.cost_price for item in SaleItem.objects(sale__in=recent_sales_ids))
                
    gross_profit = revenue_mtd - cogs_mtd
    net_profit_before_tax = gross_profit - op_expenses_mtd
    
    # Income Tax Provision (30%)
    tax_provision = max(0, net_profit_before_tax * 0.30)
    net_profit_after_tax = net_profit_before_tax - tax_provision
    
    return render_template('reports/p_and_l.html',
                           sales_mtd=sales_mtd_total,
                           revenue_mtd=revenue_mtd,
                           vat_collected=vat_collected_mtd,
                           cogs_mtd=cogs_mtd,
                           gross_profit=gross_profit,
                           expenses_mtd=op_expenses_mtd,
                           vat_paid=vat_paid_mtd,
                           net_profit_before_tax=net_profit_before_tax,
                           tax_provision=tax_provision,
                           net_profit_after_tax=net_profit_after_tax,
                           start_date=start_of_month,
                           end_date=today)
