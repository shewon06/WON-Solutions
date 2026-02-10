-- Manual Migration SQL Dump
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
	id INTEGER NOT NULL, 
	username VARCHAR(80) NOT NULL, 
	password VARCHAR(200) NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	role VARCHAR(20), 
	PRIMARY KEY (id), 
	UNIQUE (username)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` (`id`, `username`, `password`, `name`, `role`) VALUES (1, 'admin', '$2b$12$lUPx4LDDSgijvC01Fo6M3.YWBzVS1TjhR7J9J7t1BWaG4Es24QY7G', 'System Admin', 'OWNER');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `supplier` (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	phone VARCHAR(20), 
	email VARCHAR(100), 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	phone VARCHAR(20), 
	credit_balance FLOAT, address VARCHAR(300), 
	PRIMARY KEY (id), 
	UNIQUE (phone)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` (`id`, `name`, `phone`, `credit_balance`, `address`) VALUES (1, 'Kaveesha Shewon', '0705505052', 0.0, '255A Sri dhammaloka mawatha udugampola');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expense`
--

DROP TABLE IF EXISTS `expense`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `expense` (
	id INTEGER NOT NULL, 
	description VARCHAR(200) NOT NULL, 
	amount FLOAT NOT NULL, 
	category VARCHAR(50), 
	created_at DATETIME NULL, vat_amount FLOAT DEFAULT 0.0, expense_date DATE, is_paid TINYINT(1) DEFAULT 1, 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `product` (
	id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	sku VARCHAR(50), 
	barcode VARCHAR(50), 
	category_id INTEGER, 
	cost_price FLOAT NOT NULL, 
	selling_price FLOAT NOT NULL, 
	stock_qty INTEGER, 
	low_stock_threshold INTEGER, 
	supplier_id INTEGER, 
	is_active TINYINT(1), 
	PRIMARY KEY (id), 
	UNIQUE (sku), 
	UNIQUE (barcode), 
	FOREIGN KEY(category_id) REFERENCES category (id), 
	FOREIGN KEY(supplier_id) REFERENCES supplier (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` (`id`, `name`, `sku`, `barcode`, `category_id`, `cost_price`, `selling_price`, `stock_qty`, `low_stock_threshold`, `supplier_id`, `is_active`) VALUES (1, 'Sample 1', '001', NULL, '', 100.0, 200.0, 9, 5, NULL, 1);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale`
--

DROP TABLE IF EXISTS `sale`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sale` (
	id INTEGER NOT NULL, 
	customer_id INTEGER, 
	total_amount FLOAT NOT NULL, 
	payment_type VARCHAR(20), 
	created_at DATETIME NULL, 
	sold_by VARCHAR(100), subtotal FLOAT DEFAULT 0.0, vat_amount FLOAT DEFAULT 0.0, tax_amount FLOAT DEFAULT 0.0, is_vat_inclusive TINYINT(1) DEFAULT 1, 
	PRIMARY KEY (id), 
	FOREIGN KEY(customer_id) REFERENCES customer (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale`
--

LOCK TABLES `sale` WRITE;
/*!40000 ALTER TABLE `sale` DISABLE KEYS */;
INSERT INTO `sale` (`id`, `customer_id`, `total_amount`, `payment_type`, `created_at`, `sold_by`, `subtotal`, `vat_amount`, `tax_amount`, `is_vat_inclusive`) VALUES (1, 1, 200.0, 'CASH', '2026-02-05 05:38:28.003957', 'System Admin', 200.0, 0.0, 30.0, 1);
/*!40000 ALTER TABLE `sale` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sale_item`
--

DROP TABLE IF EXISTS `sale_item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sale_item` (
	id INTEGER NOT NULL, 
	sale_id INTEGER, 
	product_id INTEGER, 
	quantity INTEGER NOT NULL, 
	price FLOAT NOT NULL, cost_price FLOAT DEFAULT 0.0, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sale_id) REFERENCES sale (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sale_item`
--

LOCK TABLES `sale_item` WRITE;
/*!40000 ALTER TABLE `sale_item` DISABLE KEYS */;
INSERT INTO `sale_item` (`id`, `sale_id`, `product_id`, `quantity`, `price`, `cost_price`) VALUES (1, 1, 1, 1, 200.0, 100.0);
/*!40000 ALTER TABLE `sale_item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_settings`
--

DROP TABLE IF EXISTS `system_settings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_settings` (
	id INTEGER NOT NULL, 
	company_name VARCHAR(200), 
	tagline VARCHAR(200), 
	address VARCHAR(300), 
	phone VARCHAR(20), 
	receipt_footer VARCHAR(500), 
	currency VARCHAR(10), business_type TEXT, nature_of_business TEXT, directors TEXT, country TEXT, tax_rate REAL, 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_settings`
--

LOCK TABLES `system_settings` WRITE;
/*!40000 ALTER TABLE `system_settings` DISABLE KEYS */;
INSERT INTO `system_settings` (`id`, `company_name`, `tagline`, `address`, `phone`, `receipt_footer`, `currency`, `business_type`, `nature_of_business`, `directors`, `country`, `tax_rate`) VALUES (1, 'WON SOLUTIONS (PVT) LTD', 'Smart Digital Futures', '255A, Pathaha Road, Udugampola, Sri Lanka', '0705505052', 'Thank you for your business!', 'LKR', NULL, NULL, NULL, NULL, NULL);
/*!40000 ALTER TABLE `system_settings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company_master`
--

DROP TABLE IF EXISTS `company_master`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company_master` (
	id INTEGER NOT NULL, 
	company_name VARCHAR(200) NOT NULL, 
	tagline VARCHAR(200), 
	roc_number VARCHAR(100), 
	tin_number VARCHAR(100), 
	vat_number VARCHAR(100), 
	is_vat_registered TINYINT(1), 
	registered_address VARCHAR(500), 
	financial_year_end VARCHAR(20), 
	nature_of_business VARCHAR(500), 
	contact_email VARCHAR(100), 
	contact_phone VARCHAR(20), 
	country VARCHAR(100), 
	currency VARCHAR(10), 
	receipt_footer VARCHAR(500), website_domain VARCHAR(200), 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company_master`
--

LOCK TABLES `company_master` WRITE;
/*!40000 ALTER TABLE `company_master` DISABLE KEYS */;
INSERT INTO `company_master` (`id`, `company_name`, `tagline`, `roc_number`, `tin_number`, `vat_number`, `is_vat_registered`, `registered_address`, `financial_year_end`, `nature_of_business`, `contact_email`, `contact_phone`, `country`, `currency`, `receipt_footer`, `website_domain`) VALUES (1, 'WON SOLUTIONS (PVT) LTD', 'digital solutions', 'None', 'None', 'None', 0, 'None', 'March', 'e-commerce services, digital solutions, marketing services,
product sourcing, and related lawful business activities.', 'shewon.ksh123@gmail.com', '0705505052', 'Sri Lanka', 'LKR', 'None', NULL);
/*!40000 ALTER TABLE `company_master` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bank_transaction`
--

DROP TABLE IF EXISTS `bank_transaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bank_transaction` (
	id INTEGER NOT NULL, 
	transaction_date DATE NOT NULL, 
	description VARCHAR(500), 
	reference VARCHAR(100), 
	debit FLOAT, 
	credit FLOAT, 
	balance FLOAT, 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `document_log`
--

DROP TABLE IF EXISTS `document_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `document_log` (
	id INTEGER NOT NULL, 
	doc_type VARCHAR(100) NOT NULL, 
	doc_name VARCHAR(200), 
	file_path VARCHAR(500), 
	generated_at DATETIME NULL, 
	status VARCHAR(20), 
	financial_year VARCHAR(20), 
	PRIMARY KEY (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `document_log`
--

LOCK TABLES `document_log` WRITE;
/*!40000 ALTER TABLE `document_log` DISABLE KEYS */;
INSERT INTO `document_log` (`id`, `doc_type`, `doc_name`, `file_path`, `generated_at`, `status`, `financial_year`) VALUES (1, 'IRD_FORM_20', 'Form20_2026_REG.pdf', 'static\generated_docs\Form20_2026_REG.pdf', '2026-02-05 05:39:38.679747', 'FINAL', '2026');
/*!40000 ALTER TABLE `document_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financial_year_lock`
--

DROP TABLE IF EXISTS `financial_year_lock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `financial_year_lock` (
	id INTEGER NOT NULL, 
	year_period VARCHAR(20), 
	is_locked TINYINT(1), 
	locked_at DATETIME NULL, 
	locked_by VARCHAR(100), 
	PRIMARY KEY (id), 
	UNIQUE (year_period)
);
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `director`
--

DROP TABLE IF EXISTS `director`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `director` (
	id INTEGER NOT NULL, 
	company_id INTEGER, 
	name VARCHAR(200) NOT NULL, 
	nic_or_passport VARCHAR(50), 
	address VARCHAR(500), 
	appointment_date DATE, 
	is_active TINYINT(1), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company_master (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `director`
--

LOCK TABLES `director` WRITE;
/*!40000 ALTER TABLE `director` DISABLE KEYS */;
INSERT INTO `director` (`id`, `company_id`, `name`, `nic_or_passport`, `address`, `appointment_date`, `is_active`) VALUES (1, 1, 'H.H.D. Kaveesha Shewon Hettiarachchi', '200610201146', '255/A Pathaha road udugampola gampaha', '2006-04-11', 1);
/*!40000 ALTER TABLE `director` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shareholder`
--

DROP TABLE IF EXISTS `shareholder`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shareholder` (
	id INTEGER NOT NULL, 
	company_id INTEGER, 
	name VARCHAR(200) NOT NULL, 
	shares_count INTEGER, 
	share_class VARCHAR(50), 
	PRIMARY KEY (id), 
	FOREIGN KEY(company_id) REFERENCES company_master (id)
);
/*!40101 SET character_set_client = @saved_cs_client */;


/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
