-- Product Triggers
CREATE TRIGGER Product_Update_Trigger
ON Products
AFTER UPDATE
AS
BEGIN
    DECLARE @HistoryID INT;

    SELECT @HistoryID = ISNULL(MAX(product_history_id), 0) + 1 FROM ProductHistory;

    INSERT INTO ProductHistory (product_history_id, product_id, name, price, change_type)
    SELECT 
        @HistoryID, 
        d.product_id, 
        d.name AS old_name, 
        d.price AS old_price, 
        'UPDATE (Before)'
    FROM deleted d
    INNER JOIN inserted i ON d.product_id = i.product_id;
END;

CREATE TRIGGER Product_Delete_Trigger
ON Products
AFTER DELETE
AS
BEGIN
    DECLARE @HistoryID INT;

    SELECT @HistoryID = ISNULL(MAX(product_history_id), 0) + 1 FROM ProductHistory;

    INSERT INTO ProductHistory (product_history_id, product_id, name, price, change_type)
    SELECT 
        @HistoryID, 
        d.product_id, 
        d.name AS deleted_name, 
        d.price AS deleted_price, 
        'DELETE'
    FROM deleted d;
END;

-- Employee Triggers
CREATE TRIGGER UpdateEmployee_Trigger
ON Employees
AFTER UPDATE
AS
BEGIN
    DECLARE @EmployeeHistoryID INT;

    DECLARE @MaxHistoryID INT;
    SELECT @MaxHistoryID = ISNULL(MAX(employee_history_id), 0) FROM EmployeeHistory;

    INSERT INTO EmployeeHistory (employee_history_id, employee_id, name, contact_info, employee_type, action_type)
    SELECT 
        @MaxHistoryID + ROW_NUMBER() OVER (ORDER BY d.employee_id), 
        d.employee_id, 
        d.name AS old_name, 
        d.contact_info AS old_contact_info, 
        d.employee_type AS old_employee_type, 
        'UPDATE (Before)'
    FROM deleted d
    INNER JOIN inserted i ON d.employee_id = i.employee_id;
END;

CREATE TRIGGER DeleteEmployee_Trigger
ON Employees
AFTER DELETE
AS
BEGIN
    INSERT INTO EmployeeHistory (employee_history_id, employee_id, name, contact_info, employee_type, action_type)
    SELECT 
        ISNULL((SELECT MAX(employee_history_id) FROM EmployeeHistory), 0) + 1,
        employee_id, 
        name, 
        contact_info, 
        employee_type, 
        'DELETE'
    FROM deleted;
END;

-- Sales Triggers
CREATE TRIGGER UpdateSalesHistory_Trigger
ON Sales
AFTER UPDATE
AS
BEGIN
    INSERT INTO SalesHistory (sales_history_id, sale_id, product_id, customer_id, quantity, sale_date, action_type)
    SELECT 
        ISNULL((SELECT MAX(sales_history_id) FROM SalesHistory), 0) + 1,
        d.sales_id,
        d.product_id,
        d.customer_id,
        d.quantity,
        d.date,
        'UPDATE'
    FROM deleted d;
END;

CREATE TRIGGER DeleteSalesHistory_Trigger
ON Sales
AFTER DELETE
AS
BEGIN
    INSERT INTO SalesHistory (sales_history_id, sale_id, product_id, customer_id, quantity, sale_date, action_type)
    SELECT 
        ISNULL((SELECT MAX(sales_history_id) FROM SalesHistory), 0) + 1,
        d.sales_id,
        d.product_id,
        d.customer_id,
        d.quantity,
        d.date,
        'DELETE'
    FROM deleted d;
END;