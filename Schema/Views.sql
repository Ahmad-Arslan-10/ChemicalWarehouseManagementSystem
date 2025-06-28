CREATE VIEW SalesReturnAnalysis AS
SELECT sr.sales_return_id,
       sr.return_date,
       s.sales_id,
       p.name AS product_name,
       sr.quantity_returned
FROM SalesReturn sr
JOIN Sales s ON sr.sales_id = s.sales_id
JOIN Products p ON s.product_id = p.product_id;

CREATE VIEW SalesDetails AS
    SELECT s.sales_id, s.date, s.quantity, s.total_price, c.name AS CustomerName, p.name AS ProductName
    FROM Sales s
    JOIN Customers c ON s.customer_id = c.customer_id
    JOIN Products p ON s.product_id = p.product_id;

CREATE VIEW InventoryDetails AS
    SELECT i.inventory_id, p.name AS ProductName, i.quantity_available
    FROM Inventory i
    JOIN Products p ON i.product_id = p.product_id;

CREATE VIEW AverageOrderValueByCustomer AS
SELECT c.name AS CustomerName, AVG(s.total_price) AS AvgOrderValue
FROM Customers c
JOIN Sales s ON c.customer_id = s.customer_id
GROUP BY c.name;