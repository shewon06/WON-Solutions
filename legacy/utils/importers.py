import pandas as pd
import io
from models import Product, Category, db
import logging

logger = logging.getLogger(__name__)

def process_daraz_items(items):
    """
    Common logic to process a list of product dictionaries from Daraz (CSV or API).
    Each item should have: 'sku', 'name', 'price', 'qty', 'category_name'
    """
    imported_count = 0
    updated_count = 0
    errors = []

    for index, item in enumerate(items):
        try:
            sku = str(item.get('sku', '')).strip()
            name = str(item.get('name', '')).strip()
            price = float(item.get('price', 0))
            qty = int(item.get('qty', 0))
            category_name = str(item.get('category_name', '')).strip()

            if not sku:
                errors.append(f"Item {index+1}: Missing SKU")
                continue

            # Check for existing product by SKU
            product = Product.objects(sku=sku).first()

            if product:
                # Update existing product
                if name:
                    product.name = name
                product.selling_price = price
                product.stock_qty = qty
                
                if category_name:
                    category_obj = Category.objects(name=category_name).first()
                    if not category_obj:
                        category_obj = Category(name=category_name)
                        category_obj.save()
                    product.category = category_obj
                
                product.save()
                updated_count += 1
            else:
                # Create new product - Name is required for new products
                if not name:
                    errors.append(f"Item {index+1}: SKU {sku} is new but Name is missing in file.")
                    continue

                # Handle Category for new product
                category_obj = None
                if category_name:
                    category_obj = Category.objects(name=category_name).first()
                    if not category_obj:
                        category_obj = Category(name=category_name)
                        category_obj.save()

                new_product = Product(
                    name=name,
                    sku=sku,
                    selling_price=price,
                    cost_price=0.0,
                    stock_qty=qty,
                    category=category_obj
                )
                new_product.save()
                imported_count += 1

        except Exception as e:
            errors.append(f"Item {index+1}: {str(e)}")
            logger.error(f"Error processing Daraz item: {str(e)}")

    return {
        'imported': imported_count,
        'updated': updated_count,
        'errors': errors
    }

def import_daraz_products(file_data, file_extension):
    """
    Parses Daraz product export file (CSV or XLSX) and imports products.
    """
    try:
        if file_extension.lower() == '.csv':
            df = pd.read_csv(io.BytesIO(file_data))
        elif file_extension.lower() in ['.xlsx', '.xls']:
            try:
                # Daraz files often have instructions in the first few rows.
                # We'll try to find the row that contains 'Seller SKU' or 'SellerSKU'
                # and use that as our header.
                
                # First, read without header to inspect
                temp_df = pd.read_excel(io.BytesIO(file_data), header=None)
                header_row = 0
                for i, row in temp_df.iterrows():
                    row_values = [str(val).strip() for val in row.values]
                    if any(val in ['Seller SKU', 'SellerSKU', 'Seller Sku'] for val in row_values):
                        header_row = i
                        break
                
                # Re-read with the correct header row
                df = pd.read_excel(io.BytesIO(file_data), header=header_row)
            except Exception as e:
                logger.error(f"Excel read error: {e}")
                return {'success': False, 'message': 'Failed to read Excel file structure.'}
        else:
            return {'success': False, 'message': f'Unsupported file extension: {file_extension}'}

        # Normalize column names
        df.columns = [str(c).strip() for c in df.columns]

        # Aliases Mapping
        sku_cols = ['Seller SKU', 'SellerSKU', 'Seller Sku', 'sku']
        name_cols = ['Name', 'Product Name', 'name']
        price_cols = ['Price', 'Retail Price', 'Price (LKR)', 'price', '*Price']
        qty_cols = ['Quantity', 'Stock', 'Availability', 'qty', '*Quantity']
        cat_cols = ['Category', 'Category Name', 'category']

        def get_col(options):
            for opt in options:
                if opt in df.columns:
                    return opt
            return None

        sku_col = get_col(sku_cols)
        name_col = get_col(name_cols)
        price_col = get_col(price_cols)
        qty_col = get_col(qty_cols)
        cat_col = get_col(cat_cols)

        if not sku_col:
            return {'success': False, 'message': "Could not find 'Seller SKU' column. Please ensure you are using a standard Daraz export file."}

        items = []
        for index, row in df.iterrows():
            items.append({
                'sku': row.get(sku_col, ''),
                'name': row.get(name_col, '') if name_col else '',
                'price': row.get(price_col, 0) if price_col else 0,
                'qty': row.get(qty_col, 0) if qty_col and pd.notnull(row.get(qty_col)) else 0,
                'category_name': row.get(cat_col, '') if cat_col else ''
            })

        processed = process_daraz_items(items)
        
        # Build detailed message if there are errors
        message = f"Imported: {processed['imported']}, Updated: {processed['updated']}"
        if processed['errors']:
            unique_errors = list(set(processed['errors']))[:3] # Show first 3 unique errors
            err_summary = "; ".join(unique_errors)
            message += f". Errors ({len(processed['errors'])}): {err_summary}"
            if len(processed['errors']) > 3:
                message += " ..."

        return {
            'success': True,
            'imported': processed['imported'],
            'updated': processed['updated'],
            'errors': processed['errors'],
            'message': message
        }

    except Exception as e:
        logger.exception("Failed to parse Daraz import file")
        return {'success': False, 'message': f"Critical Error: {str(e)}"}
