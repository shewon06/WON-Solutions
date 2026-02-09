from flask_mongoengine import MongoEngine
from flask_login import UserMixin
from datetime import datetime

db = MongoEngine()

class User(UserMixin, db.Document):
    username = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)
    name = db.StringField(required=True)
    role = db.StringField(default='STAFF') # OWNER, ADMIN, STAFF, ACCOUNTANT
    
    meta = {'collection': 'users'}

class Category(db.Document):
    name = db.StringField(required=True, unique=True)
    
    meta = {'collection': 'categories'}

class Supplier(db.Document):
    name = db.StringField(required=True)
    phone = db.StringField()
    email = db.StringField()
    
    meta = {'collection': 'suppliers'}

class Product(db.Document):
    name = db.StringField(required=True)
    sku = db.StringField(unique=True)
    barcode = db.StringField(unique=True)
    category = db.ReferenceField('Category')
    cost_price = db.FloatField(required=True)
    selling_price = db.FloatField(required=True)
    stock_qty = db.IntField(default=0)
    low_stock_threshold = db.IntField(default=5)
    supplier = db.ReferenceField('Supplier')
    is_active = db.BooleanField(default=True)
    
    meta = {'collection': 'products'}

class Customer(db.Document):
    name = db.StringField(required=True)
    phone = db.StringField(unique=True)
    address = db.StringField()
    credit_balance = db.FloatField(default=0.0)
    
    meta = {'collection': 'customers'}

class Sale(db.Document):
    customer = db.ReferenceField('Customer')
    total_amount = db.FloatField(required=True)
    subtotal = db.FloatField(default=0.0)
    vat_amount = db.FloatField(default=0.0)
    tax_amount = db.FloatField(default=0.0)
    is_vat_inclusive = db.BooleanField(default=True)
    payment_type = db.StringField(default='CASH') # CASH, CARD, CREDIT
    created_at = db.DateTimeField(default=datetime.utcnow)
    sold_by = db.StringField()
    # We can embed items or use ReferenceField. 
    # To keep routes simpler for now, we'll keep SaleItem as a separate collection but linked.
    
    meta = {'collection': 'sales'}

class SaleItem(db.Document):
    sale = db.ReferenceField('Sale', required=True)
    product = db.ReferenceField('Product', required=True)
    quantity = db.IntField(required=True)
    price = db.FloatField(required=True) # Selling price at time of sale
    cost_price = db.FloatField(default=0.0) # Cost price at time of sale
    
    meta = {'collection': 'sale_items'}

class Expense(db.Document):
    description = db.StringField(required=True)
    amount = db.FloatField(required=True)
    vat_amount = db.FloatField(default=0.0)
    category = db.StringField() # Rent, Utilities, Salary, etc.
    expense_date = db.DateTimeField(default=datetime.utcnow)
    created_at = db.DateTimeField(default=datetime.utcnow)
    is_paid = db.BooleanField(default=True)
    
    meta = {'collection': 'expenses'}

class CompanyMaster(db.Document):
    company_name = db.StringField(required=True)
    tagline = db.StringField()
    roc_number = db.StringField()
    tin_number = db.StringField()
    vat_number = db.StringField()
    is_vat_registered = db.BooleanField(default=False)
    registered_address = db.StringField()
    financial_year_end = db.StringField(default='March')
    nature_of_business = db.StringField()
    contact_email = db.StringField()
    contact_phone = db.StringField()
    country = db.StringField(default='Sri Lanka')
    currency = db.StringField(default='LKR')
    website_domain = db.StringField()
    receipt_footer = db.StringField()
    
    meta = {'collection': 'company_master'}

class Director(db.Document):
    company = db.ReferenceField('CompanyMaster')
    name = db.StringField(required=True)
    nic_or_passport = db.StringField()
    address = db.StringField()
    appointment_date = db.DateTimeField()
    is_active = db.BooleanField(default=True)
    
    meta = {'collection': 'directors'}

class Shareholder(db.Document):
    company = db.ReferenceField('CompanyMaster')
    name = db.StringField(required=True)
    shares_count = db.IntField(default=0)
    share_class = db.StringField(default='Ordinary')
    
    meta = {'collection': 'shareholders'}

class BankTransaction(db.Document):
    transaction_date = db.DateTimeField(required=True)
    description = db.StringField()
    reference = db.StringField()
    debit = db.FloatField(default=0.0)
    credit = db.FloatField(default=0.0)
    balance = db.FloatField(default=0.0)
    
    meta = {'collection': 'bank_transactions'}

class DocumentLog(db.Document):
    doc_type = db.StringField(required=True) # e.g., Form 18, Share Cert, P&L
    doc_name = db.StringField()
    file_path = db.StringField()
    generated_at = db.DateTimeField(default=datetime.utcnow)
    status = db.StringField(default='DRAFT') # DRAFT, FINAL, FILED
    financial_year = db.StringField()
    
    meta = {'collection': 'document_logs'}

class FinancialYearLock(db.Document):
    year_period = db.StringField(unique=True) # e.g., "2023-2024"
    is_locked = db.BooleanField(default=False)
    locked_at = db.DateTimeField()
    locked_by = db.StringField()
    
    meta = {'collection': 'financial_year_locks'}
