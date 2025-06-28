-- Customer Procedures
CREATE PROCEDURE InsertCustomer
    @CustomerID INT,
    @Name VARCHAR(255),
    @Address VARCHAR(255),
    @ContactInfo VARCHAR(11)
AS
BEGIN
    INSERT INTO Customers (customer_id, name, address, contact_info)
    VALUES (@CustomerID, @Name, @Address, @ContactInfo);
END;

CREATE PROCEDURE UpdateCustomer
    @CustomerID INT,
    @Name VARCHAR(255),
    @Address VARCHAR(255),
    @ContactInfo VARCHAR(11)
AS
BEGIN
    UPDATE Customers
    SET name = @Name,
        address = @Address,
        contact_info = @ContactInfo
    WHERE customer_id = @CustomerID;
END;

CREATE PROCEDURE DeleteCustomer
    @CustomerID INT
AS
BEGIN
    DELETE FROM Customers
    WHERE customer_id = @CustomerID;
END;

-- Supplier Procedures
CREATE PROCEDURE InsertSupplier
    @SupplierID INT,
    @Name VARCHAR(255),
    @ContactInfo VARCHAR(11)
AS
BEGIN
    INSERT INTO Suppliers (supplier_id, name, contact_info)
    VALUES (@SupplierID, @Name, @ContactInfo);
END;

CREATE PROCEDURE UpdateSupplier
    @SupplierID INT,
    @Name VARCHAR(255),
    @ContactInfo VARCHAR(255)
AS
BEGIN
    UPDATE Suppliers
    SET name = @Name,
        contact_info = @ContactInfo
    WHERE supplier_id = @SupplierID;
END;

CREATE PROCEDURE DeleteSupplier
    @SupplierID INT
AS
BEGIN
    DELETE FROM Suppliers
    WHERE supplier_id = @SupplierID;
END;

-- Product Procedures
CREATE PROCEDURE InsertProduct
    @ProductID INT,
    @Name VARCHAR(255),
    @Price DECIMAL(10, 2)
AS
BEGIN
    INSERT INTO Products (product_id, name, price)
    VALUES (@ProductID, @Name, @Price);
END;

CREATE PROCEDURE UpdateProduct
    @ProductID INT,
    @Name VARCHAR(255),
    @Price DECIMAL(10, 2)
AS
BEGIN
    UPDATE Products
    SET name = @Name,
        price = @Price
    WHERE product_id = @ProductID;
END;

CREATE PROCEDURE DeleteProduct
    @ProductID INT
AS
BEGIN
    DELETE FROM Products
    WHERE product_id = @ProductID;
END;

-- Inventory Procedure
CREATE PROCEDURE UpdateInventory
    @ProductId INT,
    @Quantity INT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Inventory WHERE product_id = @ProductId)
    BEGIN
        UPDATE Inventory
        SET quantity_available = quantity_available + @Quantity
        WHERE product_id = @ProductId;
    END
    ELSE
    BEGIN
        INSERT INTO Inventory (inventory_id, product_id, quantity_available)
    VALUES ((SELECT ISNULL(MAX(inventory_id), 0) + 1 FROM Inventory), @ProductId, @Quantity);
    END
END;

-- Sales Procedures
CREATE PROCEDURE InsertSale
    @SalesId INT,
    @Date DATE,
    @Quantity INT,
    @CustomerId INT,
    @ProductId INT,
    @EmployeeId INT
AS
BEGIN
    DECLARE @Price DECIMAL(10, 2), @TotalPrice DECIMAL(10, 2), @InventoryAvailable INT;

    SELECT @InventoryAvailable = quantity_available 
    FROM Inventory 
    WHERE product_id = @ProductId;

    IF @InventoryAvailable >= @Quantity
    BEGIN
        SELECT @Price = price 
        FROM Products 
        WHERE product_id = @ProductId;

        SET @TotalPrice = @Price * @Quantity;

        INSERT INTO Sales (sales_id, date, quantity, total_price, employee_id, customer_id, product_id)
        VALUES (@SalesId, @Date, @Quantity, @TotalPrice, @EmployeeId, @CustomerId, @ProductId);

        DECLARE @AdjustedQuantity INT;
        SET @AdjustedQuantity = -@Quantity;
        EXEC UpdateInventory @ProductId, @AdjustedQuantity;
    END
    ELSE
    BEGIN
        RAISERROR ('Insufficient inventory available for sale.', 16, 1);
    END
END;

CREATE PROCEDURE UpdateSale
    @SalesId INT,
    @Date DATE,
    @Quantity INT,
    @CustomerId INT,
    @ProductId INT,
    @EmployeeId INT
AS
BEGIN
    DECLARE @OldQuantity INT, @OldProductId INT;
    SELECT @OldQuantity = quantity, @OldProductId = product_id 
    FROM Sales WHERE sales_id = @SalesId;

    EXEC UpdateInventory @OldProductId, @OldQuantity;

    DECLARE @InventoryAvailable INT;
    SELECT @InventoryAvailable = quantity_available 
    FROM Inventory 
    WHERE product_id = @ProductId;

    IF @InventoryAvailable >= @Quantity
    BEGIN
        
        DECLARE @Price DECIMAL(10, 2), @TotalPrice DECIMAL(10, 2);
        SELECT @Price = price FROM Products WHERE product_id = @ProductId;
        SET @TotalPrice = @Price * @Quantity;

        UPDATE Sales
        SET date = @Date,
            quantity = @Quantity,
            total_price = @TotalPrice,
            employee_id = @EmployeeId,
            customer_id = @CustomerId,
            product_id = @ProductId
        WHERE sales_id = @SalesId;

        DECLARE @AdjustedQuantity INT;
        SET @AdjustedQuantity = -@Quantity;
        EXEC UpdateInventory @ProductId, @AdjustedQuantity;
    END
    ELSE
    BEGIN
     
        DECLARE @OldAdjustedQuantity INT;
        SET @OldAdjustedQuantity = -@OldQuantity;
        EXEC UpdateInventory @OldProductId, @OldAdjustedQuantity;
        RAISERROR ('Insufficient inventory available for updated sale.', 16, 1);
    END
END;

CREATE PROCEDURE DeleteSale
    @SalesId INT
AS
BEGIN
    DECLARE @Quantity INT;
    DECLARE @ProductId INT;

    SELECT @Quantity = quantity, @ProductId = product_id
    FROM Sales
    WHERE sales_id = @SalesId;

    DELETE FROM Sales
    WHERE sales_id = @SalesId;

    EXEC UpdateInventory @ProductId, @Quantity;
END;

-- Raw Material Procedures
CREATE PROCEDURE Insert_Raw_Material (
    @material_id INT,
    @name VARCHAR(255),
    @supplier_id INT
)
AS
BEGIN
    INSERT INTO Raw_Material (material_id, name, supplier_id)
    VALUES (@material_id, @name, @supplier_id);
END;

CREATE PROCEDURE Update_Raw_Material
    @MaterialID INT,
    @Name VARCHAR(255),
    @SupplierID INT
AS
BEGIN
    UPDATE Raw_Material
    SET name = @Name,
        supplier_id = @SupplierID
    WHERE material_id = @MaterialID;
END;

CREATE PROCEDURE Delete_Raw_Material
    @MaterialID INT
AS
BEGIN
    DELETE FROM Raw_Material
    WHERE material_id = @MaterialID;
END;

-- Purchase Procedures
CREATE PROCEDURE InsertPurchase 
    @purchase_id INT,
    @date DATE,
    @quantity INT,
    @price_per_unit DECIMAL(10, 2),
    @total_price DECIMAL(10, 2),
    @employee_id INT,
    @supplier_id INT,
    @material_id INT
AS
BEGIN
    INSERT INTO Purchases (purchase_id, date, quantity, price_per_unit, total_price, employee_id, supplier_id, material_id)
    VALUES (@purchase_id, @date, @quantity, @price_per_unit, @total_price, @employee_id, @supplier_id, @material_id);
    
    -- Add purchased materials to inventory
    EXEC UpdateInventory @material_id, @quantity;
END;

CREATE PROCEDURE UpdatePurchase
    @PurchaseID INT,
    @Date DATE,
    @Quantity INT,
    @PricePerUnit DECIMAL(10, 2),
    @TotalPrice DECIMAL(10, 2),
    @EmployeeID INT,
    @SupplierID INT,
    @MaterialID INT
AS
BEGIN
    DECLARE @OldQuantity INT, @OldMaterialID INT;
    
    -- Get old values
    SELECT @OldQuantity = quantity, @OldMaterialID = material_id
    FROM Purchases 
    WHERE purchase_id = @PurchaseID;

    -- Calculate missing values if needed
    IF (@Quantity IS NOT NULL AND @PricePerUnit IS NOT NULL)
    BEGIN
        SET @TotalPrice = @Quantity * @PricePerUnit;
    END
    ELSE IF (@Quantity IS NOT NULL AND @TotalPrice IS NOT NULL)
    BEGIN
        SET @PricePerUnit = @TotalPrice / @Quantity;
    END
    ELSE IF (@PricePerUnit IS NOT NULL AND @TotalPrice IS NOT NULL)
    BEGIN
        SET @Quantity = @TotalPrice / @PricePerUnit;
    END

    DECLARE @NegativeOldQuantity INT;
    SET @NegativeOldQuantity = -@OldQuantity;
    EXEC UpdateInventory @OldMaterialID, @NegativeOldQuantity;

    UPDATE Purchases
    SET date = @Date,
        quantity = @Quantity,
        price_per_unit = @PricePerUnit,
        total_price = @TotalPrice,
        employee_id = @EmployeeID,
        supplier_id = @SupplierID,
        material_id = @MaterialID
    WHERE purchase_id = @PurchaseID;
    
    EXEC UpdateInventory @MaterialID, @Quantity;
END;

CREATE PROCEDURE DeletePurchase
    @PurchaseID INT
AS
BEGIN
    DECLARE @Quantity INT, @MaterialID INT;
    
    SELECT @Quantity = quantity, @MaterialID = material_id
    FROM Purchases
    WHERE purchase_id = @PurchaseID;

    DELETE FROM Purchases
    WHERE purchase_id = @PurchaseID;
    
    DECLARE @NegativeQuantity INT;
    SET @NegativeQuantity = -@Quantity;
    EXEC UpdateInventory @MaterialID, @NegativeQuantity;
END;

-- Production Procedures 
CREATE PROCEDURE InsertProduction
    @production_id INT,
    @date DATE,
    @product_id INT,
    @quantity_produced INT,
    @employee_id INT,
    @material_id INT
AS
BEGIN
    INSERT INTO Production (production_id, date, product_id, quantity_produced, employee_id, material_id)
    VALUES (@production_id, @date, @product_id, @quantity_produced, @employee_id, @material_id);

    EXEC UpdateInventory @product_id, @quantity_produced;

    SELECT @production_id AS production_id;
END;

CREATE PROCEDURE UpdateProduction
    @production_id INT,
    @date DATE,
    @quantity_produced INT,
    @product_id INT,
    @employee_id INT,
    @material_id INT
AS
BEGIN
    DECLARE @previous_product_id INT;
    DECLARE @previous_quantity_produced INT;

    SELECT @previous_product_id = product_id, @previous_quantity_produced = quantity_produced 
    FROM Production WHERE production_id = @production_id;

    UPDATE Production
    SET date = @date,
        quantity_produced = @quantity_produced,
        product_id = @product_id,
        employee_id = @employee_id,
        material_id = @material_id
    WHERE production_id = @production_id;

    DECLARE @negated_previous_quantity_produced INT;
    SET @negated_previous_quantity_produced = -@previous_quantity_produced;
    EXEC UpdateInventory @previous_product_id, @negated_previous_quantity_produced;

    EXEC UpdateInventory @product_id, @quantity_produced;
END;

CREATE PROCEDURE DeleteProduction
    @ProductionID INT
AS
BEGIN
    DECLARE @ProductID INT, @QuantityProduced INT;
    
    SELECT @ProductID = product_id, @QuantityProduced = quantity_produced
    FROM Production
    WHERE production_id = @ProductionID;
    
    DELETE FROM Production
    WHERE production_id = @ProductionID;

    DECLARE @NegativeQuantity INT;
    SET @NegativeQuantity = -@QuantityProduced;
    EXEC UpdateInventory @ProductID, @NegativeQuantity;
END;

-- Employee Procedures
CREATE PROCEDURE InsertEmployee
    @id INT,
    @name VARCHAR(255),
    @contact_info VARCHAR(255),
    @employee_type VARCHAR(100)
AS
BEGIN
    INSERT INTO Employees (employee_id, name, contact_info, employee_type)
    VALUES (@id, @name, @contact_info, @employee_type);
    
    INSERT INTO Salary (employee_id, salary)
    VALUES (@id, 
           CASE 
            WHEN @employee_type = 'Sales-Manager' THEN 65000.00
            WHEN @employee_type = 'Purchase-Manager' THEN 55000.00
            WHEN @employee_type = 'Supervisor' THEN 40000.00
            ELSE 30000.00  -- Default salary for other types
           END);
END;

CREATE PROCEDURE UpdateEmployee
    @id INT,
    @name VARCHAR(255),
    @contact_info VARCHAR(255),
    @employee_type VARCHAR(100)
AS
BEGIN
    UPDATE Employees
    SET name = @name,
        contact_info = @contact_info,
        employee_type = @employee_type
    WHERE employee_id = @id;
    
    UPDATE Salary
    SET salary = 
        CASE 
            WHEN @employee_type = 'Sales-Manager' THEN 65000.00
            WHEN @employee_type = 'Purchase-Manager' THEN 55000.00
            WHEN @employee_type = 'Supervisor' THEN 40000.00
            ELSE 30000.00  -- Default salary for other types
        END
    WHERE employee_id = @id;
END;

CREATE PROCEDURE DeleteEmployee
    @id INT
AS
BEGIN
    DELETE FROM Salary
    WHERE employee_id = @id;

    DELETE FROM Employees
    WHERE employee_id = @id;
END;

-- Sales Return Procedures
CREATE PROCEDURE InsertSalesReturn
    @return_id INT,
    @SalesId INT,
    @ReturnDate DATE,
    @QuantityReturned INT
AS
BEGIN
    INSERT INTO SalesReturn (sales_return_id, sales_id, return_date, quantity_returned)
    VALUES (@return_id, @SalesId, @ReturnDate, @QuantityReturned);
    
    DECLARE @ProductId INT;
    SELECT @ProductId = product_id FROM Sales WHERE sales_id = @SalesId;
    
    EXEC UpdateInventory @ProductId, @QuantityReturned;
END;

CREATE PROCEDURE UpdateSalesReturn
    @SalesReturnID INT,
    @SalesID INT,
    @ReturnDate DATE,
    @QuantityReturned INT
AS
BEGIN
    DECLARE @OldQuantityReturned INT, @OldSalesID INT, @OldProductID INT, @NewProductID INT;

    SELECT @OldQuantityReturned = quantity_returned, @OldSalesID = sales_id
    FROM SalesReturn
    WHERE sales_return_id = @SalesReturnID;

    SELECT @OldProductID = product_id
    FROM Sales
    WHERE sales_id = @OldSalesID;

    SELECT @NewProductID = product_id
    FROM Sales
    WHERE sales_id = @SalesID;

    DECLARE @NegativeOldQuantity INT;
    SET @NegativeOldQuantity = -@OldQuantityReturned;
    EXEC UpdateInventory @OldProductID, @NegativeOldQuantity;

    UPDATE SalesReturn
    SET sales_id = @SalesID,
        return_date = @ReturnDate,
        quantity_returned = @QuantityReturned
    WHERE sales_return_id = @SalesReturnID;

    EXEC UpdateInventory @NewProductID, @QuantityReturned;
END;

CREATE PROCEDURE DeleteSalesReturn
    @SalesReturnID INT
AS
BEGIN
    DECLARE @SalesID INT, @QuantityReturned INT, @ProductID INT;

    SELECT @SalesID = sales_id, @QuantityReturned = quantity_returned
    FROM SalesReturn
    WHERE sales_return_id = @SalesReturnID;

    SELECT @ProductID = product_id
    FROM Sales
    WHERE sales_id = @SalesID;

    DELETE FROM SalesReturn
    WHERE sales_return_id = @SalesReturnID;

    DECLARE @NegativeQuantityReturned INT;
    SET @NegativeQuantityReturned = -@QuantityReturned;
    EXEC UpdateInventory @ProductID, @NegativeQuantityReturned;
END;

-- Purchase Return Procedures
CREATE PROCEDURE InsertPurchaseReturn
    @PurchaseReturnId INT,
    @PurchaseId INT,
    @ReturnDate DATE,
    @QuantityReturned INT
AS
BEGIN
    INSERT INTO PurchaseReturn (purchase_return_id, purchase_id, return_date, quantity_returned)
    VALUES (@PurchaseReturnId, @PurchaseId, @ReturnDate, @QuantityReturned);

    DECLARE @MaterialID INT;
    SELECT @MaterialID = material_id FROM Purchases WHERE purchase_id = @PurchaseId;
    
    DECLARE @NegativeQuantity INT;
    SET @NegativeQuantity = -@QuantityReturned;
    EXEC UpdateInventory @MaterialID, @NegativeQuantity;
END;

CREATE PROCEDURE UpdatePurchaseReturn
    @PurchaseReturnID INT,
    @PurchaseID INT,
    @ReturnDate DATE,
    @QuantityReturned INT
AS
BEGIN
    DECLARE @OldQuantityReturned INT, @OldPurchaseID INT, @OldMaterialID INT, @NewMaterialID INT;
    
    SELECT @OldQuantityReturned = quantity_returned, @OldPurchaseID = purchase_id
    FROM PurchaseReturn 
    WHERE purchase_return_id = @PurchaseReturnID;
    
    SELECT @OldMaterialID = material_id
    FROM Purchases
    WHERE purchase_id = @OldPurchaseID;

    IF @OldMaterialID IS NULL
    BEGIN
        RAISERROR('Purchase return record not found.', 16, 1);
        RETURN;
    END
    
    SELECT @NewMaterialID = material_id
    FROM Purchases
    WHERE purchase_id = @PurchaseID;

    IF @NewMaterialID IS NULL
    BEGIN
        RAISERROR('New purchase record not found.', 16, 1);
        RETURN;
    END

    EXEC UpdateInventory @OldMaterialID, @OldQuantityReturned;
    
    UPDATE PurchaseReturn
    SET purchase_id = @PurchaseID,
        return_date = @ReturnDate,
        quantity_returned = @QuantityReturned
    WHERE purchase_return_id = @PurchaseReturnID;
 
    DECLARE @NegativeNewQuantity INT;
    SET @NegativeNewQuantity = -@QuantityReturned;
    EXEC UpdateInventory @NewMaterialID, @NegativeNewQuantity;
END;

CREATE PROCEDURE DeletePurchaseReturn
    @PurchaseReturnID INT
AS
BEGIN
    DECLARE @PurchaseID INT, @QuantityReturned INT, @MaterialID INT;
    
    SELECT @PurchaseID = purchase_id, @QuantityReturned = quantity_returned
    FROM PurchaseReturn 
    WHERE purchase_return_id = @PurchaseReturnID;
    
    SELECT @MaterialID = material_id
    FROM Purchases
    WHERE purchase_id = @PurchaseID;

    IF @MaterialID IS NULL
    BEGIN
        RAISERROR('Purchase return record not found.', 16, 1);
        RETURN;
    END

    DELETE FROM PurchaseReturn
    WHERE purchase_return_id = @PurchaseReturnID;
    
    EXEC UpdateInventory @MaterialID, @QuantityReturned;
END;

-- Report Procedures
CREATE PROCEDURE TotalSalesReportByProduct
AS
BEGIN
    SELECT p.name AS Product_Name,
           SUM(s.quantity) AS Total_Quantity_Sold,
           SUM(s.total_price) AS Total_Revenue
    FROM Products p
    INNER JOIN Sales s ON p.product_id = s.product_id
    GROUP BY p.name
    ORDER BY Total_Revenue DESC;
END;

CREATE PROCEDURE SalesSummaryByCustomer
AS
BEGIN
    SELECT c.name AS CustomerName, 
           COUNT(*) AS TotalSales, 
           SUM(s.total_price) AS TotalRevenue
    FROM Customers c
    JOIN Sales s ON c.customer_id = s.customer_id
    GROUP BY c.name
    ORDER BY TotalRevenue DESC;
END;

CREATE PROCEDURE TopSellingProducts
AS
BEGIN
    SELECT TOP 5 p.name AS ProductName, 
           SUM(s.quantity) AS TotalSales
    FROM Products p
    JOIN Sales s ON p.product_id = s.product_id
    GROUP BY p.name
    ORDER BY TotalSales DESC;
END;

CREATE PROCEDURE PurchaseSummaryBySupplier
AS
BEGIN
    SELECT s.name AS SupplierName, 
           COUNT(*) AS TotalPurchases, 
           SUM(p.total_price) AS TotalSpent  
    FROM Suppliers s
    JOIN Purchases p ON s.supplier_id = p.supplier_id
    GROUP BY s.name
    ORDER BY TotalSpent DESC;
END;

CREATE PROCEDURE TotalRevenueByMonth
AS
BEGIN
    SELECT YEAR(date) AS Year, 
           MONTH(date) AS Month, 
           SUM(total_price) AS TotalRevenue
    FROM Sales
    GROUP BY YEAR(date), MONTH(date)
    ORDER BY Year, Month;
END;