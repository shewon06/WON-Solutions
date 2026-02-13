import sqlite3
import os
import shutil

def cleanup():
    db_path = 'instance/system.db'
    docs_dir = 'static/generated_docs'
    
    # 1. Clear Database Tables
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            tables_to_clear = [
                'document_log',
                'sale',
                'sale_item',
                'expense',
                'bank_transaction',
                'product',
                'customer',
                'supplier',
                'category'
            ]
            
            for table in tables_to_clear:
                print(f"Clearing table: {table}")
                cursor.execute(f"DELETE FROM {table};")
                
            conn.commit()
            conn.close()
            print("Database cleanup successful.")
        except Exception as e:
            print(f"Error cleaning database: {e}")
    else:
        print("Database not found.")

    # 2. Clear Generated Documents
    if os.path.exists(docs_dir):
        try:
            print(f"Cleaning directory: {docs_dir}")
            for filename in os.listdir(docs_dir):
                file_path = os.path.join(docs_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                        print(f"Deleted file: {filename}")
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        print(f"Deleted directory: {filename}")
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
            print("Document cleanup successful.")
        except Exception as e:
            print(f"Error cleaning documents: {e}")
    else:
        print("Documents directory not found.")

if __name__ == '__main__':
    cleanup()
