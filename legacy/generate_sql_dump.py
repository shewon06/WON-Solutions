import sqlite3
import os

def export_for_mysql():
    sqlite_path = 'system.db'
    output_path = 'manual_migration.sql'
    
    if not os.path.exists(sqlite_path):
        print(f"Error: {sqlite_path} not found.")
        return

    print(f"Reading data from {sqlite_path} (High Compatibility Mode v3)...")
    sl_conn = sqlite3.connect(sqlite_path)
    sl_cursor = sl_conn.cursor()

    # Get all tables and their creation SQL
    sl_cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table';")
    table_data = sl_cursor.fetchall()

    with open(output_path, 'w', encoding='utf-8') as f:
        # Standard MySQL Dump Headers with proper variable initialization
        f.write("-- Manual Migration SQL Dump\n")
        f.write("/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;\n")
        f.write("/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;\n")
        f.write("/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;\n")
        f.write("/*!40101 SET NAMES utf8mb4 */;\n")
        f.write("/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;\n")
        f.write("/*!40103 SET TIME_ZONE='+00:00' */;\n")
        f.write("/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;\n")
        f.write("/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;\n")
        f.write("/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;\n")
        f.write("/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;\n\n")

        for table, create_sql in table_data:
            if table in ('sqlite_sequence', 'alembic_version'):
                continue

            print(f"Exporting table: {table}")
            
            # MySQL conversion logic
            mysql_create = create_sql.replace('DATETIME', 'DATETIME NULL')
            mysql_create = mysql_create.replace('BOOLEAN', 'TINYINT(1)')
            # Remove sqlite-specific check constraints
            import re
            mysql_create = re.sub(r'CHECK\s*\([^)]+\)', '', mysql_create)
            mysql_create = mysql_create.replace('AUTOINCREMENT', 'AUTO_INCREMENT')
            
            # Ensure backticks
            if not f"`{table}`" in mysql_create:
                mysql_create = mysql_create.replace(f'CREATE TABLE {table}', f'CREATE TABLE `{table}`')
                mysql_create = mysql_create.replace(f'CREATE TABLE "{table}"', f'CREATE TABLE `{table}`')

            f.write(f"--\n-- Table structure for table `{table}`\n--\n\n")
            f.write(f"DROP TABLE IF EXISTS `{table}`;\n")
            f.write(f"/*!40101 SET @saved_cs_client     = @@character_set_client */;\n")
            f.write(f"/*!40101 SET character_set_client = utf8 */;\n")
            f.write(f"{mysql_create.strip()};\n")
            f.write(f"/*!40101 SET character_set_client = @saved_cs_client */;\n\n")

            # Data
            sl_cursor.execute(f"PRAGMA table_info({table})")
            columns = [c[1] for c in sl_cursor.fetchall()]
            col_names = ", ".join([f"`{c}`" for c in columns])

            sl_cursor.execute(f"SELECT * FROM {table}")
            rows = sl_cursor.fetchall()

            if rows:
                f.write(f"--\n-- Dumping data for table `{table}`\n--\n\n")
                f.write(f"LOCK TABLES `{table}` WRITE;\n")
                f.write(f"/*!40000 ALTER TABLE `{table}` DISABLE KEYS */;\n")
                
                # Multi-row insert is better for MySQL
                values_list = []
                for row in rows:
                    vals = []
                    for val in row:
                        if val is None:
                            vals.append("NULL")
                        elif isinstance(val, (int, float)):
                            vals.append(str(val))
                        else:
                            escaped = str(val).replace("'", "''")
                            vals.append(f"'{escaped}'")
                    values_list.append(f"({', '.join(vals)})")
                
                # Split into chunks of 100 for safety
                chunk_size = 100
                for i in range(0, len(values_list), chunk_size):
                    chunk = values_list[i:i + chunk_size]
                    f.write(f"INSERT INTO `{table}` ({col_names}) VALUES {', '.join(chunk)};\n")
                
                f.write(f"/*!40000 ALTER TABLE `{table}` ENABLE KEYS */;\n")
                f.write(f"UNLOCK TABLES;\n")
            
            f.write("\n")

        # Footer
        f.write("/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;\n")
        f.write("/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;\n")
        f.write("/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;\n")
        f.write("/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;\n")
        f.write("/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;\n")
        f.write("/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;\n")
        f.write("/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;\n")
        f.write("/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;\n")

    sl_conn.close()
    print(f"Successfully generated {output_path} with fixed headers.")

if __name__ == '__main__':
    export_for_mysql()
