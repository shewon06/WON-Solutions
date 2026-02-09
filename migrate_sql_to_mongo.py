import sqlite3
import os
from dotenv import load_dotenv
import flask.json
try:
    from flask.json import JSONEncoder
except ImportError:
    import json
    class JSONEncoder(json.JSONEncoder):
        pass
    flask.json.JSONEncoder = JSONEncoder

from mongoengine import connect
from models import (
    User, Category, Supplier, Product, Customer, Sale, SaleItem, 
    Expense, CompanyMaster, Director, Shareholder, BankTransaction, 
    DocumentLog, FinancialYearLock
)
from datetime import datetime

# Load env for MONGODB_URI
load_dotenv(override=True)

def migrate():
    sqlite_path = 'system.db'
    if not os.path.exists(sqlite_path):
        print(f"Error: {sqlite_path} not found.")
        return

    mongo_uri = os.getenv('MONGODB_URI')
    if not mongo_uri:
        print("Error: MONGODB_URI not found.")
        return

    print("Connecting to MongoDB Atlas...")
    connect(host=mongo_uri)

    sl_conn = sqlite3.connect(sqlite_path)
    sl_conn.row_factory = sqlite3.Row
    sl_cursor = sl_conn.cursor()

    print("--- Starting Migration ---")

    # 1. Users
    print("Migrating Users...")
    sl_cursor.execute("SELECT * FROM user")
    for row in sl_cursor.fetchall():
        if not User.objects(username=row['username']).first():
            User(username=row['username'], password=row['password'], 
                 name=row['name'], role=row['role']).save()

    # 2. Categories
    print("Migrating Categories...")
    category_map = {} # SQL ID -> Mongo Object
    sl_cursor.execute("SELECT * FROM category")
    for row in sl_cursor.fetchall():
        cat = Category.objects(name=row['name']).first()
        if not cat:
            cat = Category(name=row['name']).save()
        category_map[row['id']] = cat

    # 3. Suppliers
    print("Migrating Suppliers...")
    supplier_map = {} # SQL ID -> Mongo Object
    sl_cursor.execute("SELECT * FROM supplier")
    for row in sl_cursor.fetchall():
        sup = Supplier.objects(name=row['name']).first()
        if not sup:
            sup = Supplier(name=row['name'], phone=row['phone'], email=row['email']).save()
        supplier_map[row['id']] = sup

    # 4. Products
    print("Migrating Products...")
    product_map = {} # SQL ID -> Mongo Object
    sl_cursor.execute("SELECT * FROM product")
    for row in sl_cursor.fetchall():
        prod = Product.objects(sku=row['sku']).first()
        if not prod:
            prod = Product(
                name=row['name'], sku=row['sku'], barcode=row['barcode'],
                category=category_map.get(row['category_id']),
                cost_price=row['cost_price'], selling_price=row['selling_price'],
                stock_qty=row['stock_qty'], low_stock_threshold=row['low_stock_threshold'],
                supplier=supplier_map.get(row['supplier_id']),
                is_active=bool(row['is_active'])
            ).save()
        product_map[row['id']] = prod

    # 5. Customers
    print("Migrating Customers...")
    customer_map = {} # SQL ID -> Mongo Object
    sl_cursor.execute("SELECT * FROM customer")
    for row in sl_cursor.fetchall():
        cust = Customer.objects(phone=row['phone']).first()
        if not cust:
            cust = Customer(name=row['name'], phone=row['phone'], 
                            address=row['address'], credit_balance=row['credit_balance']).save()
        customer_map[row['id']] = cust

    # 6. CompanyMaster
    print("Migrating Company Settings...")
    sl_cursor.execute("SELECT * FROM company_master")
    for row in sl_cursor.fetchall():
        if not CompanyMaster.objects().first():
            CompanyMaster(
                company_name=row['company_name'], tagline=row['tagline'],
                roc_number=row['roc_number'], tin_number=row['tin_number'],
                vat_number=row['vat_number'], is_vat_registered=bool(row['is_vat_registered']),
                registered_address=row['registered_address'], contact_email=row['contact_email'],
                contact_phone=row['contact_phone'], country=row['country'],
                currency=row['currency'], website_domain=row['website_domain'],
                receipt_footer=row['receipt_footer']
            ).save()

    # 7. Sales
    print("Migrating Sales...")
    sale_map = {} # SQL ID -> Mongo Object
    sl_cursor.execute("SELECT * FROM sale")
    for row in sl_cursor.fetchall():
        # Using ID mapping is hard because SQL IDs are just integers
        # We'll just migrate them all (assume fresh mongo)
        created_at = datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S.%f') if row['created_at'] else datetime.utcnow()
        sale = Sale(
            customer=customer_map.get(row['customer_id']),
            total_amount=row['total_amount'], subtotal=row['subtotal'],
            vat_amount=row['vat_amount'], tax_amount=row['tax_amount'],
            is_vat_inclusive=bool(row['is_vat_inclusive']),
            payment_type=row['payment_type'], created_at=created_at,
            sold_by=row['sold_by']
        ).save()
        sale_map[row['id']] = sale

    # 8. SaleItems
    print("Migrating Sale Items...")
    sl_cursor.execute("SELECT * FROM sale_item")
    for row in sl_cursor.fetchall():
        SaleItem(
            sale=sale_map.get(row['sale_id']),
            product=product_map.get(row['product_id']),
            quantity=row['quantity'], price=row['price'],
            cost_price=row['cost_price']
        ).save()

    # 9. Expenses
    print("Migrating Expenses...")
    sl_cursor.execute("SELECT * FROM expense")
    for row in sl_cursor.fetchall():
        Expense(
            description=row['description'], amount=row['amount'],
            vat_amount=row['vat_amount'], category=row['category'],
            expense_date=datetime.strptime(row['expense_date'], '%Y-%m-%d') if row['expense_date'] else None,
            created_at=datetime.strptime(row['created_at'], '%Y-%m-%d %H:%M:%S.%f') if row['created_at'] else datetime.utcnow(),
            is_paid=bool(row['is_paid'])
        ).save()

    # 10. FinancialYearLock
    print("Migrating Financial Locks...")
    sl_cursor.execute("SELECT * FROM financial_year_lock")
    for row in sl_cursor.fetchall():
        if not FinancialYearLock.objects(year_period=row['year_period']).first():
            FinancialYearLock(
                year_period=row['year_period'], is_locked=bool(row['is_locked']),
                locked_at=datetime.strptime(row['locked_at'], '%Y-%m-%d %H:%M:%S.%f') if row['locked_at'] else None,
                locked_by=row['locked_by']
            ).save()

    print("--- Migration Finished Successfully! ---")
    sl_conn.close()

if __name__ == '__main__':
    migrate()
