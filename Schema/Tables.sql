-- Customers Table
CREATE TABLE Customers (
    customer_id INT,
    name VARCHAR(255),
    address VARCHAR(255),
    contact_info VARCHAR(11),
    CONSTRAINT pk_customer PRIMARY KEY (customer_id)
);

-- Suppliers Table
CREATE TABLE Suppliers (
    supplier_id INT,
    name VARCHAR(255),
    contact_info VARCHAR(255),
    CONSTRAINT pk_suppliers PRIMARY KEY(supplier_id)
);

-- Products Table
CREATE TABLE Products (
    product_id INT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    CONSTRAINT pk_products PRIMARY KEY(product_id)
);

-- Employees Table
CREATE TABLE Employees (
    employee_id INT,
    name VARCHAR(255),
    contact_info VARCHAR(255),
    employee_type VARCHAR(100),
    CONSTRAINT pk_employees PRIMARY KEY (employee_id)
);

-- Inventory Table
CREATE TABLE Inventory (
    inventory_id INT,
    product_id INT,
    quantity_available INT,
    CONSTRAINT pk_inventory PRIMARY KEY (inventory_id),
    CONSTRAINT fk_product_in_inventory FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Sales Table
CREATE TABLE Sales(
    sales_id INT,
    date DATE,
    quantity INT,
    total_price DECIMAL(10, 2),
    employee_id INT,
    customer_id INT,
    product_id INT,
    CONSTRAINT pk_sales PRIMARY KEY (sales_id),
    CONSTRAINT fk_employee_in_sales FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    CONSTRAINT fk_customer_in_sales FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    CONSTRAINT fk_product_in_sales FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Raw Material Table
CREATE TABLE Raw_Material (
    material_id INT,
    name VARCHAR(255),
    supplier_id INT,
    CONSTRAINT pk_raw_materials PRIMARY KEY (material_id),
    CONSTRAINT fk_suppliers_in_raw_material FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id)
);

-- Purchases Table
CREATE TABLE Purchases (
    purchase_id INT,
    date DATE,
    quantity INT,
    price_per_unit DECIMAL(10, 2),
    total_price DECIMAL(10, 2),
    employee_id INT,
    supplier_id INT,
    material_id INT,
    CONSTRAINT pk_purchase_id PRIMARY KEY (purchase_id),
    CONSTRAINT fk_employee_in_purchases FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    CONSTRAINT fk_supplier_in_purchases FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    CONSTRAINT fk_raw_material_in_purchases FOREIGN KEY (material_id) REFERENCES Raw_Material(material_id)
);

-- Production Table
CREATE TABLE Production (
    production_id INT,
    date DATE,
    quantity_produced INT,
    employee_id INT,
    material_id INT,
    product_id INT,
    CONSTRAINT pk_production PRIMARY KEY (production_id),
    CONSTRAINT fk_employee_in_production FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
    CONSTRAINT fk_material_id_in_production FOREIGN KEY (material_id) REFERENCES Raw_Material(material_id),
    CONSTRAINT fk_product_in_production FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

-- Salary Table
CREATE TABLE Salary (
    employee_id INT PRIMARY KEY,
    salary DECIMAL(10, 2),
    CONSTRAINT fk_employee_salary FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
);

-- Sales Return Table
CREATE TABLE SalesReturn (
    sales_return_id INT,
    sales_id INT,
    return_date DATE,
    quantity_returned INT,
    CONSTRAINT pk_sales_return PRIMARY KEY (sales_return_id),
    CONSTRAINT fk_sales_return_sales FOREIGN KEY (sales_id) REFERENCES Sales(sales_id)
);

-- Purchase Return Table
CREATE TABLE PurchaseReturn (
    purchase_return_id INT PRIMARY KEY,
    purchase_id INT,
    return_date DATE,
    quantity_returned INT,
    CONSTRAINT fk_purchase_return_purchase FOREIGN KEY (purchase_id) REFERENCES Purchases(purchase_id)
);

-- History Tables
CREATE TABLE ProductHistory (
    product_history_id INT PRIMARY KEY,
    product_id INT,
    name VARCHAR(255),
    price DECIMAL(10, 2),
    change_type VARCHAR(50)
);

CREATE TABLE EmployeeHistory (
    employee_history_id INT PRIMARY KEY,
    employee_id INT,
    name VARCHAR(255),
    contact_info VARCHAR(255),
    employee_type VARCHAR(100),
    action_type VARCHAR(50) 
);

CREATE TABLE SalesHistory (
    sales_history_id INT PRIMARY KEY,
    sale_id INT,
    product_id INT,
    customer_id INT,
    quantity INT,
    sale_date DATE,
    action_type VARCHAR(50)
);

-- Table Constraints and Check Constraints
USE CWMS;
GO

-- Customers Constraints
ALTER TABLE Customers ADD 
    CONSTRAINT CHK_CustomerIDPositive CHECK (customer_id > 0),
    CONSTRAINT CHK_Customers_Name_NotNull CHECK (name IS NOT NULL),
    CONSTRAINT CHK_Customers_Address_NotNull CHECK (address IS NOT NULL),
    CONSTRAINT CHK_Customers_ContactInfo_NotNull CHECK (contact_info IS NOT NULL);

-- Suppliers Constraints
ALTER TABLE Suppliers ADD 
    CONSTRAINT CHK_SupplierIDPositive CHECK (supplier_id > 0),
    CONSTRAINT CHK_Suppliers_Name_NotNull CHECK (name IS NOT NULL),
    CONSTRAINT CHK_Suppliers_ContactInfo_NotNull CHECK (contact_info IS NOT NULL);

-- Products Constraints
ALTER TABLE Products ADD 
    CONSTRAINT CHK_ProductIDPositive CHECK (product_id > 0),
    CONSTRAINT CHK_Products_Name_NotNull CHECK (name IS NOT NULL),
    CONSTRAINT CHK_Products_Price_NonNegative CHECK (price > 0);

-- Inventory Constraints
ALTER TABLE Inventory ADD 
    CONSTRAINT CHK_InventoryIDPositive CHECK (inventory_id > 0),
    CONSTRAINT CHK_ProductID_IN_INVENTORY_Positive CHECK (product_id > 0),
    CONSTRAINT CHK_QuantityNonNegative CHECK (quantity_available >= 0);

-- Sales Constraints
ALTER TABLE Sales ADD 
    CONSTRAINT CHK_SalesIDPositive CHECK (sales_id > 0),
    CONSTRAINT CHK_CustomerID_IN_SALES_Positive CHECK (customer_id > 0),
    CONSTRAINT CHK_ProductID_IN_SALES_Positive CHECK (product_id > 0),
    CONSTRAINT CHK_QuantityPositive CHECK (quantity > 0),
    CONSTRAINT CHK_TotalPricePositive CHECK (total_price > 0);

-- Purchases Constraints
ALTER TABLE Purchases ADD 
    CONSTRAINT CHK_Purchases_Quantity_NonNegative CHECK (quantity > 0),
    CONSTRAINT CHK_Purchases_PricePerUnit_NonNegative CHECK (price_per_unit > 0),
    CONSTRAINT CHK_Purchases_TotalPrice_NonNegative CHECK (total_price > 0);

-- Raw Material Constraints
ALTER TABLE Raw_Material ADD 
    CONSTRAINT CHK_MaterialIDPositive CHECK (material_id > 0),
    CONSTRAINT CHK_SupplierID_IN_RAW_Positive CHECK (supplier_id > 0),
    CONSTRAINT CHK_Material_Name_NotNull CHECK (name IS NOT NULL);

-- Production Constraints
ALTER TABLE Production ADD 
    CONSTRAINT CHK_ProductionIDPositive CHECK (production_id > 0),
    CONSTRAINT CHK_ProductID_IN_PRODUCTION_Positive CHECK (product_id > 0),
    CONSTRAINT CHK_QuantityProducedPositive CHECK (quantity_produced > 0);

-- Employees Constraints
ALTER TABLE Employees ADD 
    CONSTRAINT CHK_EmployeeIDPositive CHECK (employee_id > 0),
    CONSTRAINT CHK_Employee_Name_NotNull CHECK (name IS NOT NULL),
    CONSTRAINT CHK_Employee_ContactInfo_NotNull CHECK (contact_info IS NOT NULL);

-- Sales Return Constraints
ALTER TABLE SalesReturn ADD 
    CONSTRAINT CHK_SalesReturnIDPositive CHECK (sales_return_id > 0),
    CONSTRAINT CHK_SalesID_IN_RETURN_Positive CHECK (sales_id > 0),
    CONSTRAINT CHK_QuantityReturnedPositive CHECK (quantity_returned > 0);

-- Purchase Return Constraints
ALTER TABLE PurchaseReturn ADD 
    CONSTRAINT CHK_PurchaseReturnIDPositive CHECK (purchase_return_id > 0),
    CONSTRAINT CHK_PurchaseID_IN_RETURN_Positive CHECK (purchase_id > 0),
    CONSTRAINT CHK_QuantityReturned_IN_RETURN_Positive CHECK (quantity_returned > 0);